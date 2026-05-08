using Microsoft.Extensions.Logging;
using SurveillanceRegistry.Models;
using SurveillanceRegistry.Services;

using ILoggerFactory loggerFactory = LoggerFactory.Create(builder =>
    builder.AddSimpleConsole(o => { o.SingleLine = true; o.TimestampFormat = "yyyy-MM-dd HH:mm:ss "; })
           .SetMinimumLevel(LogLevel.Information));

ILogger<Registry> registryLogger = loggerFactory.CreateLogger<Registry>();
ILogger<Program>  log            = loggerFactory.CreateLogger<Program>();

var s1 = new Suspect("John Dow",   "Sleepy Dog",  "Spain", "Barcelona");
s1.AddPhoneNumber("00496955444444"); s1.AddPhoneNumber("00496955333333");

var s2 = new Suspect("Danny Rust", "Rusty Knife", "UK",    "London");
s2.AddPhoneNumber("00446999888888");

var s3 = new Suspect("Bob Robson", "Frozen Bear", "Spain", "Oslo");
s3.AddPhoneNumber("00478484777777"); s3.AddPhoneNumber("00478484666666"); s3.AddPhoneNumber("00478484222222");

Communication[] comms =
[
    new PhoneCall("00496955444444", "00478484777777", 15, 10, 2017, 127),
    new PhoneCall("00496955444444", "00478484777777", 16, 10, 2017, 240),
    new PhoneCall("00446999888888", "00496955333333", 17, 10, 2017,  52),
    new PhoneCall("00446999888888", "00478484777777", 18, 10, 2017, 180),
    new PhoneCall("00478484666666", "00496955333333", 19, 10, 2017, 305),
    new PhoneCall("00496955444444", "00478484222222", 20, 10, 2017, 247),
    new PhoneCall("00478484222222", "00496955333333", 21, 10, 2017,  32),
    new Sms("00496955444444", "00478484777777", 10, 10, 2017, "fancy a drink tonight?"),
    new Sms("00496955333333", "00446999888888", 11, 10, 2017, "Nitro Bomb prepared"),
    new Sms("00446999888888", "00496955444444", 12, 10, 2017, "flying to Berlin tomorrow"),
    new Sms("00478484777777", "00446999888888", 13, 10, 2017, "No internet connection today"),
    new Sms("00478484777777", "00446999888888", 14, 10, 2017, "Gun Received from Rusty Knife"),
    new Sms("00478484777777", "00446999888888", 15, 10, 2017, "Metro Attack ready"),
    new Sms("00478484666666", "00446999888888", 16, 10, 2017, "Explosives downtown have been placed"),
];

var registry = new Registry(registryLogger);
registry.AddSuspect(s1); registry.AddSuspect(s2); registry.AddSuspect(s3);
foreach (var c in comms) registry.AddCommunication(c);

log.LogInformation("── Test 1: Suspect with most partners ──");
var top = registry.GetSuspectWithMostPartners();
if (top is not null) log.LogInformation("{Name}, {CodeName}", top.Name, top.CodeName);

log.LogInformation("── Test 2: Longest phone call ──");
var call = registry.GetLongestPhoneCallBetween("00496955444444", "00478484777777");
if (call is not null) log.LogInformation("{Call}", call);

log.LogInformation("── Test 3: Suspicious messages ──");
foreach (var sms in registry.GetSuspiciousMessagesBetween("00478484777777", "00446999888888"))
    log.LogInformation("{Sms}", sms);

log.LogInformation("── Test 4: Connection check ──");
log.LogInformation("s1→s3: {R}", s1.IsConnectedTo(s3));
log.LogInformation("s3→s2: {R}", s3.IsConnectedTo(s2));

log.LogInformation("── Test 5: Common partners s1 & s3 ──");
foreach (var s in s1.GetCommonPartners(s3))
    log.LogInformation("{Name}, {CodeName}", s.Name, s.CodeName);

log.LogInformation("── Test 6: Suspects from Spain ──");
registry.LogSuspectsFromCountry("Spain");
