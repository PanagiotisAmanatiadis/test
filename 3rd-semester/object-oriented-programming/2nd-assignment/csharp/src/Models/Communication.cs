namespace SurveillanceGui.Models;

public abstract class Communication
{
    public string SenderNumber   { get; }
    public string ReceiverNumber { get; }
    public int Day { get; } public int Month { get; } public int Year { get; }

    protected Communication(string senderNumber, string receiverNumber, int day, int month, int year)
    { SenderNumber = senderNumber; ReceiverNumber = receiverNumber; Day = day; Month = month; Year = year; }

    public abstract int    GetDuration();
    public abstract string GetSmsContent();

    public override string ToString() =>
        $"{SenderNumber} → {ReceiverNumber} on {Year:0000}/{Month:00}/{Day:00}";
}
