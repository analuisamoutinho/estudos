// Segundo passo do login: troca o código do GitHub por um token de acesso e
// devolve para a janela que abriu o popup do painel /admin (protocolo padrão
// do Decap/Sveltia CMS para autenticação via "github" backend).
module.exports = async (req, res) => {
  const { code, error, error_description: errorDescription } = req.query || {};

  if (error) {
    res.status(400).send(`Erro de autorização do GitHub: ${errorDescription || error}`);
    return;
  }
  if (!code) {
    res.status(400).send("Faltou o parâmetro 'code' do GitHub.");
    return;
  }

  const clientId = process.env.OAUTH_GITHUB_CLIENT_ID;
  const clientSecret = process.env.OAUTH_GITHUB_CLIENT_SECRET;
  if (!clientId || !clientSecret) {
    res.status(500).send("Faltou configurar OAUTH_GITHUB_CLIENT_ID/OAUTH_GITHUB_CLIENT_SECRET no Vercel.");
    return;
  }

  const tokenResp = await fetch("https://github.com/login/oauth/access_token", {
    method: "POST",
    headers: { "Content-Type": "application/json", Accept: "application/json" },
    body: JSON.stringify({ client_id: clientId, client_secret: clientSecret, code }),
  });
  const data = await tokenResp.json();

  if (data.error || !data.access_token) {
    res.status(400).send(`Erro ao trocar o código por token: ${data.error_description || data.error || "token ausente"}`);
    return;
  }

  const payload = JSON.stringify({ token: data.access_token, provider: "github" });
  const html = `<!DOCTYPE html><html><body>
<script>
(function() {
  function receiveMessage(e) {
    window.opener.postMessage('authorization:github:success:${payload}', e.origin);
    window.removeEventListener('message', receiveMessage, false);
  }
  window.addEventListener('message', receiveMessage, false);
  window.opener.postMessage('authorizing:github', '*');
})();
</script>
</body></html>`;
  res.setHeader("Content-Type", "text/html; charset=utf-8");
  res.status(200).send(html);
};
