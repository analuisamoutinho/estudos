// Primeiro passo do login do painel /admin: redireciona para a tela de
// autorização do GitHub. Exige as variáveis de ambiente OAUTH_GITHUB_CLIENT_ID
// e OAUTH_GITHUB_CLIENT_SECRET configuradas no projeto Vercel.
module.exports = (req, res) => {
  const clientId = process.env.OAUTH_GITHUB_CLIENT_ID;
  if (!clientId) {
    res.status(500).send("Falta configurar OAUTH_GITHUB_CLIENT_ID no Vercel.");
    return;
  }
  const host = req.headers.host;
  const redirectUri = `https://${host}/api/callback`;
  const url =
    "https://github.com/login/oauth/authorize" +
    `?client_id=${encodeURIComponent(clientId)}` +
    `&redirect_uri=${encodeURIComponent(redirectUri)}` +
    "&scope=" + encodeURIComponent("repo,user");
  res.writeHead(302, { Location: url });
  res.end();
};
