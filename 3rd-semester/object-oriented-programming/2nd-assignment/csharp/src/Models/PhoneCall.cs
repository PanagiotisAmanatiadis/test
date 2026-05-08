namespace SurveillanceGui.Models;

public sealed class PhoneCall : Communication
{
    public int DurationSeconds { get; }

    public PhoneCall(string senderNumber, string receiverNumber,
                     int day, int month, int year, int durationSeconds)
        : base(senderNumber, receiverNumber, day, month, year)
        => DurationSeconds = durationSeconds;

    public override int    GetDuration()   => DurationSeconds;
    public override string GetSmsContent() => string.Empty;
    public override string ToString() =>
        $"PhoneCall[{base.ToString()}, duration={DurationSeconds}s]";
}
