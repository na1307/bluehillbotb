using System.Text.Json;

namespace BluehillBotB.Emergency;

public sealed record class UserProfile(string UserName, JsonElement Groups);
