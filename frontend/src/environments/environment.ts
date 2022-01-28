/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'https://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'mycoffeeshop-project.us', // the auth0 domain prefix
    audience: 'coffee', // the audience set for the auth0 app
    clientId: 'H64dADXV5aPw5kujJbK8QznXDXI7ENfu', // the client id generated for the auth0 app
    callbackURL: 'https://localhost:8100', // the base url of the running ionic application.
  }
};
