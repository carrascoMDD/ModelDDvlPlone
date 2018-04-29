fi_open = context.fi_open
fi_read = context.fi_read
fi_write = context.fi_write
fi_close = context.fi_close
os_join = context.os_join

# Import a standard function, and get the HTML request and response objects.
from Products.PythonScripts.standard import html_quote
request = container.REQUEST
RESPONSE =  request.RESPONSE

f= fi_open(os_join(path, name), "w")
fi_write(f, file.read())
fi_close(f)
