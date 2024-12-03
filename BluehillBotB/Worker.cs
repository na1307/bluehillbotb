using System.Text.RegularExpressions;
using WikiClientLibrary;
using WikiClientLibrary.Generators;
using WikiClientLibrary.Pages;

namespace BluehillBotB;

public static class Worker {
    private static readonly Regex deletePattern = new(@"\{\{(삭제 ?(신|요)청|삭신?|ㅅ{1,2}|ㅆ|del(ete)?|speedy(delete)?)\|",
        RegexOptions.IgnoreCase | RegexOptions.Compiled);

    private static readonly Regex uncategorizedPattern = new(@"\{\{(분류( ?필요| 없음)|uncategorized)\}\}\n?",
        RegexOptions.IgnoreCase | RegexOptions.Compiled);

    public static async Task RemoveUncategorizedTemplate(CancellationToken token = default) {
        using SiteLoginManager manager = new();

        await manager.LoginAsync();

        try {
            await foreach (var page in new CategoryMembersGenerator(manager.Site, "분류:분류 필요 문서").EnumPagesAsync()
                               .WithCancellation(token)) {
                await page.RefreshAsync(PageQueryOptions.FetchContent, token);

                var baseText = page.Content;

                if (baseText is not null && deletePattern.IsMatch(baseText)) {
                    var newText = uncategorizedPattern.Replace(baseText, string.Empty);

                    Console.WriteLine(
                        $"Title: \"{page.Title}\"{Environment.NewLine}New Text:{Environment.NewLine}{newText}");

// I hate you Rider, because it does not fit my format
#pragma warning disable IDE0055
                    if (!await page.EditAsync(new() {
                            Content = newText,
                            Summary = "봇: 삭제 신청된 문서에서 분류 필요 틀 제거",
                            Minor = true,
                            Bot = true
                        })) {
#pragma warning restore IDE0055
                        throw new OperationFailedException();
                    }
                } else {
                    Console.WriteLine($"Page \"{page.Title}\" does not have a Deletion template.");
                }
            }
        } finally {
            await manager.LogoutAsync();
        }
    }
}
