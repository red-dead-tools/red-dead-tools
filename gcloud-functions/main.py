from red_dead import export


# Based on:
# https://cloud.google.com/functions/docs/writing/http#handling_cors_requests
def cors_enabled_function(request, get_body, headers=None):
    # For more information about CORS and CORS preflight requests, see
    # https://developer.mozilla.org/en-US/docs/Glossary/Preflight_request
    # for more information.

    headers = headers or {}
    # Set CORS headers for the preflight request
    if request.method == 'OPTIONS':
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            **headers,
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }

        return ('', 204, headers)

    # Set CORS headers for the main request
    headers = {
        **headers,
        'Access-Control-Allow-Origin': '*'
    }

    return (get_body(request), 200, headers)


def get_export_data(request):
    sheet_name = request.args.get('sheet_name')
    settings = export.get_settings(sheet_name=sheet_name)
    return settings.as_export()


def red_dead_tools(request):
    filename = export.get_export_filename()

    headers = {'Content-Disposition': f'attachment; filename="{filename}"'}
    return cors_enabled_function(request, get_export_data, headers)
