using System.ComponentModel.DataAnnotations;

namespace BluehillBotB.Emergency;

public sealed class SubmitData(string userName) {
    public string UserName { get; } = userName;

    [Required]
    public string Reason { get; set; } = string.Empty;
}
