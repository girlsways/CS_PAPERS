
from __future__ import annotations

import typing as t

from graphene_django.constants import MUTATION_ERRORS_FLAG
from graphene_django.utils.utils import set_rollback
from graphene_django.views import GraphQLView as BaseGraphQLView

if t.TYPE_CHECKING:
    from django.http.request import HttpRequest


class GraphQLView(BaseGraphQLView):
    def get_response(
        self,
        request: HttpRequest,
        data: t.Dict[str, t.Any],
        show_graphiql: bool = False,
    ):
        """
        It is extremely hard to return a status code that is not 200 or 400, which means
        we can't use mechanisms that work out of the box, like 401 and 403 with standard
        frontend libraries. This is because GraphQL does not just work over HTTP but
        also websockets for example and errors can be chained.

        Of course, this doesn't apply to a Django served HTTP view (allthough chaining
        is still possible, it is not very productive for applications behind an
        authentication wall, to allow more queries if one returns authentication error,
        but so far I haven't found a short-circuit mechanism that can stop the resolve
        chain).

        So what we do here, is return the highest status code and this is complicated by
        the fact that exceptions get promoted to GraphQLLocatedError without fully
        copying all slots of the orinal error, so we need to look for our status_code
        attribute on the original error as well.

        :param request: Http request as provided by Django
        :param data: POST data, parsed from json to python dict
        :param show_graphiql: bool indicating if we show the graphiql interface.
        :return:
        """
        query, variables, operation_name, ID = self.get_graphql_params(request, data)

        execution_result = self.execute_graphql_request(
            request, data, query, variables, operation_name, show_graphiql
        )

        if getattr(request, MUTATION_ERRORS_FLAG, False) is True:
            set_rollback()

        status_code = 200
        if execution_result:
            response = {}

            if execution_result.errors:
                set_rollback()
                response["errors"] = [
                    self.format_error(e) for e in execution_result.errors
                ]
                # Look for the highest status code that upstream exceptions provided.
                status_code = max(
                    *[getattr(e, "status_code", 0) for e in execution_result.errors],
                    *[
                        getattr(e.original_error, "status_code", 0)
                        for e in execution_result.errors
                        if hasattr(e, "original_error")
                    ],
                    status_code,
                )

            # Stay compatible for invalid data/input
            if execution_result.invalid:
                status_code = 400
            else:
                response["data"] = execution_result.data

            if self.batch:
                response["id"] = ID
                response["status"] = status_code

            result = self.json_encode(request, response, pretty=show_graphiql)
        else:
            result = None

        return result, status_code