using BluehillBotB.Emergency;
using BluehillBotB.Emergency.Components;
using Microsoft.Extensions.FileProviders;

var builder = WebApplication.CreateBuilder(args);

builder.Configuration.SetBasePath(AppContext.BaseDirectory).AddJsonFile("appsettings.json");

// Add services to the container.
builder.Services.AddHttpContextAccessor()
    .AddHttpClient()
    .AddDistributedMemoryCache()
    .AddSession(options => options.IdleTimeout = TimeSpan.FromMinutes(30))
    .AddRazorComponents()
    .AddInteractiveServerComponents();

builder.Services.AddScoped<MediaWikiOAuthService>();

var app = builder.Build();

app.UseSession();

// Configure the HTTP request pipeline.
if (!app.Environment.IsDevelopment()) {
    app.UseExceptionHandler("/Error", createScopeForErrors: true);

    app.UseStaticFiles(new StaticFileOptions {
        FileProvider = new PhysicalFileProvider(Path.Combine(AppContext.BaseDirectory, "wwwroot")),
    });
} else {
    app.UseStaticFiles();
}

app.UseRouting();

app.UseAntiforgery();

app.MapRazorComponents<App>()
    .AddInteractiveServerRenderMode();

// OAuth callback endpoint
app.MapGet("/oauth-callback", async (HttpContext http, MediaWikiOAuthService oauthService) => {
    var query = http.Request.Query;
    string code = query["code"]!;
    string? error = query["error"];

    if (!string.IsNullOrEmpty(code)) {
        // Exchange authorization code for access token
        var accessToken = await oauthService.ExchangeCodeForTokenAsync(code);

        // Store token in session or database
        http.Session.SetString("AccessToken", accessToken);

        // Redirect user back to home page or a protected page
        http.Response.Redirect("/");
    } else if (!string.IsNullOrEmpty(error) && error == "unauthorized_client") {
        // Just redirect user back to home page
        http.Response.Redirect("/");
    } else {
        http.Response.StatusCode = 400;
    }
});

// Submit endpoint
app.MapPost("/submit", (SubmitData submitData) => {
    app.Logger.LogInformation("UserName: {UserName}, Reason: {Reason}", submitData.UserName, submitData.Reason);

    return Results.Ok("Success");
}).WithMetadata(new Microsoft.AspNetCore.Mvc.IgnoreAntiforgeryTokenAttribute());

await app.RunAsync();
