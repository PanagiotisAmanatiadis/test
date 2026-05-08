using Microsoft.Extensions.Logging;
using SurveillanceGui.Models;
using SurveillanceGui.Services;
using SurveillanceGui.UI;

using ILoggerFactory loggerFactory = LoggerFactory.Create(builder =>
    builder.AddSimpleConsole(o => { o.SingleLine = true; o.TimestampFormat = "yyyy-MM-dd HH:mm:ss "; })
           .SetMinimumLevel(LogLevel.Information));

var s1 = new Suspect("John Dow",   "Sleepy Dog",  "Spain",  "Barcelona");
s1.AddPhoneNumber("00496955444444"); s1.AddPhoneNumber("00496955333333");
var s2 = new Suspect("Danny Rust", "Rusty Knife", "UK",     "London");
s2.AddPhoneNumber("00446999888888");
var s3 = new Suspect("Bob Robson", "Frozen Bear", "Spain",  "Oslo");
s3.AddPhoneNumber("00478484777777"); s3.AddPhoneNumber("00478484666666"); s3.AddPhoneNumber("00478484222222");
var s4 = new Suspect("John Papas", "Quick Knife", "Greece", "Athens");
s4.AddPhoneNumber("0030210567888");

Communication[] comms =
[
    new PhoneCall("00496955444444", "00478484777777", 15, 10, 2019, 127),
    new PhoneCall("00496955444444", "00478484777777", 16, 10, 2019, 240),
    new PhoneCall("00446999888888", "00496955333333", 17, 10, 2019,  52),
    new PhoneCall("00446999888888", "00478484777777", 18, 10, 2019, 180),
    new PhoneCall("00478484666666", "00496955333333", 19, 10, 2019, 305),
    new PhoneCall("00496955444444", "00478484222222", 20, 10, 2019, 247),
    new PhoneCall("00478484222222", "00496955333333", 21, 10, 2019,  32),
    new Sms("00496955444444", "00478484777777", 10, 10, 2019, "fancy a drink tonight?"),
    new Sms("00496955333333", "00446999888888", 11, 10, 2019, "Nitro Bomb prepared"),
    new Sms("00446999888888", "00496955444444", 12, 10, 2019, "flying to Berlin tomorrow"),
    new Sms("00478484777777", "00446999888888", 13, 10, 2019, "No internet connection today"),
    new Sms("00478484777777", "00446999888888", 14, 10, 2019, "Gun Received from Rusty Knife"),
    new Sms("00478484777777", "00446999888888", 15, 10, 2019, "Metro Attack ready"),
    new Sms("00478484666666", "00446999888888", 16, 10, 2019, "Explosives downtown have been placed"),
    new Sms("0030210567888",  "00478484222222", 22, 10, 2019, "Meet you at Oslo"),
];

var registry = new Registry(loggerFactory.CreateLogger<Registry>());
foreach (var s in new[] { s1, s2, s3, s4 }) registry.AddSuspect(s);
foreach (var c in comms) registry.AddCommunication(c);

new ConsoleUI(registry, loggerFactory.CreateLogger<ConsoleUI>()).Run();
