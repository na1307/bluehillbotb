using IdentityModel.Client;
using System.Text.Json;

namespace BluehillBotB.Emergency;

public sealed class MediaWikiOAuthService(IConfiguration config, IHttpClientFactory httpClientFactory) {
    private static readonly Uri callbackUrl = new("https://bluehillbotb.toolforge.org/oauth-callback");

    private static readonly JsonSerializerOptions jsOptions = new() {
        PropertyNameCaseInsensitive = true
    };

    public Uri BuildAuthorizationUrl() {
        var aep = config["MediaWiki:AuthorizationEndpoint"]!;

        Dictionary<string, string> parameters = new() {
            ["client_id"] = config["MediaWiki:ClientId"]!,
            ["response_type"] = "code",
            ["redirect_uri"] = callbackUrl.ToString()
        };

        var qs = string.Join("&", parameters.Select(kvp => $"{kvp.Key}={Uri.EscapeDataString(kvp.Value)}"));

        return new($"{aep}?{qs}");
    }

    public async Task<string> ExchangeCodeForTokenAsync(string code) {
        using AuthorizationCodeTokenRequest authorizationCodeTokenRequest = new();
        authorizationCodeTokenRequest.Address = config["MediaWiki:TokenEndpoint"];
        authorizationCodeTokenRequest.ClientId = config["MediaWiki:ClientId"]!;
        authorizationCodeTokenRequest.ClientSecret = Environment.GetEnvironmentVariable("OAUTH_SECRET");
        authorizationCodeTokenRequest.Code = code;
        authorizationCodeTokenRequest.RedirectUri = callbackUrl.ToString();

        using var client = httpClientFactory.CreateClient();
        var tokenResponse = await client.RequestAuthorizationCodeTokenAsync(authorizationCodeTokenRequest);

        if (tokenResponse.IsError) {
            throw new("Token request error: " + tokenResponse.Error);
        }

        return tokenResponse.AccessToken!;
    }

    public async Task<UserProfile> GetUserProfileAsync(string accessToken) {
        using var client = httpClientFactory.CreateClient();

        client.DefaultRequestHeaders.Authorization = new("Bearer", accessToken);

        var response = await client.GetAsync(new Uri(config["MediaWiki:ProfileEndpoint"]!));
        response.EnsureSuccessStatusCode();

        var json = await response.Content.ReadAsStringAsync();
        var profile = JsonSerializer.Deserialize<UserProfile>(json, jsOptions);

        return profile!;
    }
}
