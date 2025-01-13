import React from "react";
import jsPDF from "jspdf";
import "jspdf-autotable";
import "./PDFGenerator.css"

const PDFGenerator = ({ playerStats, fullStats, plotImage, analysis }) => {
  const generatePDF = () => {
    const doc = new jsPDF();

    
    doc.setFontSize(18);
    doc.text("Fantasy Football Analyzer Report", 14, 20);

   
    if (playerStats) {
      doc.setFontSize(14);
      doc.text("Player Stats", 14, 30);
      doc.autoTable({
        startY: 35,
        head: [["Stat", "Value"]],
        body: Object.entries(playerStats).map(([key, value]) => [key, value]),
      });
    }

    
    if (fullStats && fullStats.length > 0) {
        const importantStats = [
          "Season", "Team", "Pos", "G", "GS", "Cmp", "Att", "Yds", "TD", "Int", "Rate", "Lng",
        ];
      
        
        const tableHeader = importantStats;
      
        
        const tableBody = fullStats.map((seasonStats) => {
          return importantStats.map((stat) => seasonStats[stat] || 'N/A');
        });
      
        
        doc.addPage();
        doc.setFontSize(14);
        doc.text("Full Stats (All Seasons)", 14, 20);
      
        doc.autoTable({
          startY: 25,
          head: [tableHeader], 
          body: tableBody,     
          styles: { fontSize: 10 },
        });
      }
      
      
      

    
    if (analysis && plotImage && analysis.length > 0 && plotImage.length > 0) {
        analysis.forEach((item, index) => {
          doc.addPage();
          doc.setFontSize(14);
          doc.text(`Analysis ${index + 1}`, 14, 20);
      
          
          doc.autoTable({
            startY: 25,
            head: [["Analysis"]],
            body: [[item]],
          });
      
          
          if (plotImage[index]) {
            const img = new Image();
            img.src = plotImage[index];
            doc.addImage(img, "JPEG", 14, 60, 180, 100);
          }
        });
      }
      
    
    doc.save("Fantasy_Football_Analyzer_Report.pdf");
  };

  return (
    <button onClick={generatePDF} className="pdfButton">
      Generate PDF
    </button>
  );
};

export default PDFGenerator;
