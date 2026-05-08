namespace SurveillanceRegistry.Models;

/// <summary>Represents an SMS text message communication.</summary>
public sealed class Sms : Communication
{
    public string Content { get; }

    public Sms(string senderNumber, string receiverNumber,
               int day, int month, int year, string content)
        : base(senderNumber, receiverNumber, day, month, year)
        => Content = content;

    public override int    GetDuration()   => 0;
    public override string GetSmsContent() => Content;

    public override string ToString() =>
        $"SMS[{base.ToString()}, content=\"{Content}\"]";
}
