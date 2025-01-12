import React, { useState, useEffect } from "react";
import "./LoadingSpinner.css";

const LoadingSpinner = () => {
  const [randomFact, setRandomFact] = useState("");

  const funFacts = [
    "The NFL was founded in 1920 and was originally called the American Professional Football Association (APFA).",
    "The Green Bay Packers are the only publicly owned franchise in the NFL.",
    "The Lombardi Trophy is named after Vince Lombardi, the legendary coach of the Green Bay Packers.",
    "The Super Bowl is the most-watched television event in the United States every year.",
    "The longest field goal in NFL history is 66 yards, kicked by Justin Tucker in 2021.",
    "Tom Brady holds the record for the most Super Bowl wins by a player, with 7 championships.",
    "The Dallas Cowboys are often referred to as 'America’s Team'.",
    "NFL games are played with a football that is 11 inches long and weighs about one pound.",
    "The Chicago Bears have retired more jersey numbers than any other team in the NFL.",
    "The NFL Draft was first held in 1936.",
    "The Pittsburgh Steelers and New England Patriots are tied for the most Super Bowl victories by a team, with 6 each.",
    "The Miami Dolphins are the only team in NFL history to complete a perfect season, going undefeated in 1972.",
    "The NFL's first televised game was broadcast in 1939 on NBC.",
    "The Arizona Cardinals are the oldest team in the NFL, founded in 1898.",
    "The Buffalo Bills went to four consecutive Super Bowls (1991–1994) but lost each one.",
    "The NFL generates over $18 billion in annual revenue, making it the richest sports league in the world.",
    "John Madden, the legendary coach and broadcaster, never had a losing season in his 10-year coaching career.",
    "The Detroit Lions and Dallas Cowboys always host games on Thanksgiving Day.",
    "An NFL game lasts about 3 hours, but the ball is in play for only about 11 minutes.",
    "The Jacksonville Jaguars and Houston Texans are the youngest NFL franchises, established in 1995 and 2002 respectively.",
    "Jerry Rice holds the record for most career receiving yards, with 22,895 yards.",
    "The Cleveland Browns are the only team to never appear in a Super Bowl.",
    "Deion Sanders is the only athlete to play in both a Super Bowl and a World Series.",
    "The NFL was the first professional sports league to implement instant replay review in 1986.",
    "The Vince Lombardi Trophy weighs about 7 pounds and is made of sterling silver.",
    "The NFL uses over 700,000 footballs each season, including preseason and playoffs.",
    "The Seattle Seahawks are the only team to play in both the NFC and AFC Championship games.",
    "Patrick Mahomes is the youngest quarterback to win a Super Bowl MVP award.",
    "The Miami Dolphins' 1972 perfect season ended with a 14-7 win over the Washington Redskins in Super Bowl VII.",
    "In 1995, the Carolina Panthers and Jacksonville Jaguars became the first expansion teams to join the NFL since 1976.",
    "The Chicago Bears have the most wins in NFL history, with over 780 victories.",
    "The Denver Broncos lost their first 4 Super Bowl appearances before winning back-to-back titles in 1997 and 1998.",
    "The Philadelphia Eagles’ 'Philly Special' trick play in Super Bowl LII helped them secure their first Super Bowl title.",
    "The New England Patriots won three Super Bowls in four years (2001, 2003, 2004), a feat only matched by the Dallas Cowboys in the 1990s.",
    "The NFL has played games internationally in London, Mexico City, and Toronto as part of its global expansion.",
    "The NFL's annual scouting combine takes place in Indianapolis, Indiana.",
    "The Oakland Raiders were the first wild-card team to win the Super Bowl in 1980.",
    "The New York Jets' only Super Bowl victory came in 1969, led by quarterback Joe Namath.",
    "The San Francisco 49ers won all five of their Super Bowl appearances, making them the only team undefeated in multiple Super Bowls (min. 3).",
    "The Atlanta Falcons blew a 28-3 lead in Super Bowl LI, losing to the Patriots in overtime.",
    "The Indianapolis Colts were originally based in Baltimore before moving to Indianapolis in 1984.",
    "The Dallas Cowboys have the most playoff wins of any NFL team.",
    "The Tampa Bay Buccaneers are the first team to win a Super Bowl in their home stadium (Super Bowl LV).",
    "The NFL introduced the salary cap in 1994 to maintain competitive balance among teams.",
    "The Houston Oilers were renamed the Tennessee Titans in 1999.",
    "Brett Favre holds the record for most consecutive starts by an NFL quarterback, with 297 games.",
    "The 2007 New England Patriots are the only team to go 16-0 in the regular season.",
    "The Minnesota Vikings have the most playoff losses in NFL history.",
    "The NFL adopted the two-point conversion rule in 1994.",
    "The New York Giants defeated the undefeated New England Patriots in Super Bowl XLII.",
    "The Buffalo Bills’ mascot is named Billy Buffalo.",
    "The NFL's headquarters are located in New York City.",
    "The St. Louis Rams moved back to Los Angeles in 2016 after 21 seasons.",
    "The Baltimore Ravens are named after Edgar Allan Poe's famous poem 'The Raven.'",
    "The Kansas City Chiefs were originally called the Dallas Texans.",
    "The NFL has 32 teams divided into two conferences: the NFC and AFC.",
    "The average career length of an NFL player is about 3.3 years.",
    "The Pittsburgh Steelers were originally called the Pittsburgh Pirates.",
    "The NFL adopted the sudden death overtime rule in 1974.",
    "The San Diego Chargers moved to Los Angeles in 2017.",
    "The first Super Bowl halftime show featured two college marching bands.",
    "The New Orleans Saints won their first Super Bowl in 2010.",
    "The NFL's Pro Bowl was first played in 1951.",
    "The Chicago Bears' George Halas coached for 40 seasons, the most in NFL history.",
    "Tony Gonzalez holds the record for most receptions by a tight end.",
    "The Detroit Lions are the only team to go 0-16 in a single season (2008).",
    "The first NFL game played outside the U.S. was in Toronto, Canada, in 1950.",
    "The NFL introduced the wild-card playoff system in 1970.",
    "The Arizona Cardinals were the first NFL team to relocate, moving to Chicago in 1920.",
    "The first Monday Night Football game was broadcast in 1970.",
    "The Tennessee Titans were once known as the Houston Oilers.",
    "Joe Montana won four Super Bowls and never threw an interception in any of them.",
    "The first dome stadium in the NFL was the Houston Astrodome.",
    "The average attendance at an NFL game is around 67,000 fans.",
    "The Buffalo Bills' Ralph Wilson was one of the founding owners of the AFL.",
    "The NFL adopted the use of instant replay challenges in 1999.",
    "Tom Dempsey, who was born without toes on his right foot, held the longest field goal record (63 yards) for 43 years.",
    "The NFL expanded to a 17-game schedule starting in 2021.",
    "The Super Bowl halftime show attracts more viewers than the game itself in some years.",
    "The New York Jets were the first team to win the Super Bowl as part of the AFL.",
    "The NFL's first African American quarterback was Fritz Pollard in the 1920s.",
    "The Los Angeles Rams were the first NFL team to put logos on their helmets.",
    "The 'Hail Mary' play was coined after a 1975 game-winning pass by Roger Staubach.",
    "The NFL introduced colored penalty flags in 1941.",
    "Lamar Jackson is the youngest quarterback to win the NFL MVP award.",
    "The Minnesota Vikings’ mascot is named Viktor the Viking.",
    "Aaron Rodgers holds the record for the best career passer rating.",
    "The Carolina Panthers' first regular-season game was in 1995."
  ];
  
  useEffect(() => {
    const fact = funFacts[Math.floor(Math.random() * funFacts.length)];
    setRandomFact(`Did you know? ${fact}`);
  }, []);

  return (
    <div className="spinnerContainer">
      <div className="loadingSpinner"></div>
      <p>Loading...</p>
      <p className="funFact">{randomFact}</p>
    </div>
  );
};

export default LoadingSpinner;

