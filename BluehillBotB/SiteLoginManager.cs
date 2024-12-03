using WikiClientLibrary.Client;
using WikiClientLibrary.Sites;

namespace BluehillBotB;

public sealed class SiteLoginManager : IDisposable {
    private readonly WikiClient client;

    public SiteLoginManager() {
        client = new() {
            ClientUserAgent = "BluehillBotB/0.0 (na1307@outlook.kr)"
        };
        Site = new(client, "https://ko.wikipedia.org/w/api.php");
    }

    public WikiSite Site { get; }

    public async Task LoginAsync() {
        await Site.Initialization;
        await Site.LoginAsync("BluehillBot B", Environment.GetEnvironmentVariable("BOT_PASSWORD")!);
    }

    public Task LogoutAsync() => Site.LogoutAsync();

    public void Dispose() => client.Dispose();
}
