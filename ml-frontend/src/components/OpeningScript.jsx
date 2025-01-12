import React, { useEffect, useState } from "react";
import "./OpeningScript.css";

const OpeningScript = ({ onComplete }) => {
  const [displayText, setDisplayText] = useState("");
  const [index, setIndex] = useState(0);
  const [showScript, setShowScript] = useState(true);

  const scriptText = `
🏈 Welcome to Fantasy Football Pro! 🏆
Are you ready to dominate your fantasy football league? Whether you're a rookie or a seasoned pro, we've got the tools, stats, and insights to give you the edge.
From player rankings to matchup projections, Fantasy Football Pro is your ultimate guide to making smarter picks and managing your team like a champion.
Let’s take your game to the next level—your league mates won’t know what hit them! 🚀
  `.trim();

  const typingSpeed = 50; 
  const typingDuration = scriptText.length * typingSpeed; 
  const fadeOutDelay = typingDuration + 2000; 

  useEffect(() => {
    if (index < scriptText.length) {
      const typingTimer = setTimeout(() => {
        setDisplayText((prev) => prev + scriptText[index]);
        setIndex((prev) => prev + 1);
      }, typingSpeed);
      return () => clearTimeout(typingTimer);
    } else {
      const scriptTimer = setTimeout(() => {
        setShowScript(false);
        if (onComplete) onComplete();
      }, 2000);
      return () => clearTimeout(scriptTimer);
    }
  }, [index, scriptText, onComplete]);

  if (!showScript) return null;

  return (
    <div className="openingScriptContainer" style={{ animationDelay: `${fadeOutDelay}ms` }}>
      <div className="openingText">
        <p>{displayText}</p>
      </div>
    </div>
  );
};

export default OpeningScript;

