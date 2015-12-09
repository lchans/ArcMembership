"""`appengine_config` gets loaded when starting a new application instance."""
import vendor
import os
# insert `lib` as a site directory so our `main` module can load
# third-party libraries, and override built-ins with newer
# versions.
vendor.add('lib')
vendor.add('views')


# Workaround the dev-environment SSL
#   http://stackoverflow.com/q/16192916/893652
if os.environ.get('SERVER_SOFTWARE', '').startswith('Development'):
    import imp
    import os.path
    from google.appengine.tools.devappserver2.python import sandbox

    sandbox._WHITE_LIST_C_MODULES += ['_ssl', '_socket']
    # Use the system socket.
    psocket = os.path.join(os.path.dirname(os.__file__), 'socket.py')
    imp.load_source('socket', psocket)