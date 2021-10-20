A Sample Python project that uses the BigFix REST API

The application, runFixlet.py, will find all fixlets that match a
pattern given by the --match parameter and will issue an action for
each matched fixlet targeting all the computers then relevant for it.

I'm not saying this is good idea!

The purpose of this is just to make use of the bigfixREST.py module,
which only has a little bit of functionality at this time, but that
I plan to expand, and hope to have active open source development
around.