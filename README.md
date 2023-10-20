### Proxy API

Create your virtual environment with `venv` and touch `.env` in the project root to set the environment variable to run `app.py`

`export FLASK_APP=app.py`

`export JWT_SECRET_KEY=<jwt-secret-key>`

you can generate a secret key on the command line using `openssl rand -base64 32`. You will also need to use this value manually in the `Authorize` section of the Swagger UI to test this API

run the flask app from within your virtualenvironment, for example with a virtualenvironment named `venv` run:

`source venv/bin/activate`

then run with `python -m flask run`


=====

### Assessment - MVP choices 

✅ = prioritized and implemented 

🗒️ = deemed premature 

⚠️ = partially implemented or tied to something implemented

✅ Rate Limiting: rate limiting at the proxy level to protect your microservice. "200 per day", "50 per hour"

⚠️ Logging & Monitoring: Implementing logging and monitoring at the proxy level can help diagnose issues, understand usage patterns, and monitor the health of both the proxy and the microservice. Additional logging framework is not implemented, because there is sufficient information coming from the API framework to the console. For scalability, an external logging can be used, which is a factor of the deployment compute instance used, such as AWS Cloudwatch

⚠️ Security - Additional security should be done at the compute instance level. Such as enforcing HTTPS, SSL and TLS. If deployed this would be inherited.

✅ Request Validation 

✅ Error Handling - see error_handler

✅ Code Structure and Design - component based architecture

✅ Authentication and Authorization - uses JWT, requests to the inference API must use the accessToken returned from the /login API endpoint in the Authorization header as `Bearer accessToken`

🗒️ Batch Processing - premature optimization

⚠️ Environment Configuration - only 1 environment at the moment. having multiple API keys or access to upstream testing environments would make this make sense

🗒️ Caching - premature optimization

🔁 Deployment - a github pages or vercel deployment is certainly possible, and it will enforce SSL/TLS

✅ Documentation - via comments, README and Swagger UI

🗒️ Asynchronous Processing - there are no long running requests here and the compute instances can scale if need be, tied to deployment

⚠️ User Management - scaffolding for this is added via the authentication framework, but the users are just hardcoded. for a real MVP I would use clerk.dev, looked into adding it here but they don't have an official python/flask framework and the hardcoding gets the point across

✅ (partial) Unit Testing - write them as you go. Login is implemented. Mocked HTTP requests are not.

🗒️ Integration Testing - premature optimization

✅ Endpoint Structure - /api/ and api/inference via post requests. other verbs are possible but the inference API has no updates to a patient or data store, only diagnosis. tree structure apt for adding the patient and embeddings API.

✅ Scalability - modular design (model, route, schema) make it easier to scale the application horizontally. each module can be further expanded. statelessness and documentation style help. low overhead of Flask helps. Could use Redis to cache requests.
