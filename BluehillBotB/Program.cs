using BluehillBotB;

if (args.Length != 1) {
    Console.WriteLine("Error: Only one parameter must be provided.");
    return 1;
}

switch (args[0]) {
    case "remove-uncategorized-template":
        await Worker.RemoveUncategorizedTemplate();
        break;

    default:
        throw new ArgumentException("Invalid argument provided.", nameof(args));
}

return 0;
