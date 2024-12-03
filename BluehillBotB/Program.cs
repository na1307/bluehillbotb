using WikiClientLibrary;
using WikiClientLibrary.Client;
using WikiClientLibrary.Pages;
using WikiClientLibrary.Sites;

using WikiClient client = new();
client.ClientUserAgent = "BluehillBotB/0.0 (na1307@outlook.kr)";
WikiSite site = new(client, "https://ko.wikipedia.org/w/api.php");

await site.Initialization;

try {
    await site.LoginAsync("BluehillBot B", Environment.GetEnvironmentVariable("BOT_PASSWORD")!);
} catch (WikiClientException ex) {
    Console.WriteLine(ex.Message);
    return;
}

WikiPage page = new(site, "초안:연습장");

await page.RefreshAsync(PageQueryOptions.FetchContent);

Console.WriteLine(await page.EditAsync(new() {
    Content = "{{연습장 안내문}}" + Environment.NewLine + "Test",
    Minor = true,
    Summary = "Test"
}));

await site.LogoutAsync();
