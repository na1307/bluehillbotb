using BluehillBotB.Emergency.Components;
using Microsoft.Extensions.FileProviders;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
builder.Services.AddRazorComponents()
    .AddInteractiveServerComponents();

var app = builder.Build();

// Configure the HTTP request pipeline.
if (!app.Environment.IsDevelopment()) {
    app.UseExceptionHandler("/Error", createScopeForErrors: true);
}

if (!app.Environment.IsDevelopment()) {
    app.UseStaticFiles(new StaticFileOptions {
        FileProvider = new PhysicalFileProvider(Path.Combine(AppContext.BaseDirectory, "wwwroot")),
    });
} else {
    app.UseStaticFiles();
}

app.UseAntiforgery();

app.MapRazorComponents<App>()
    .AddInteractiveServerRenderMode();

await app.RunAsync();
