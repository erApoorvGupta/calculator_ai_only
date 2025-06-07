"use client"; // Add this for client components in Next.js App Router

import { useRef, useEffect } from "react";
import "./MagnetLines.css"; // We will create this CSS file next

interface MagnetLinesProps {
  rows?: number;
  columns?: number;
  containerSize?: string;
  lineColor?: string;
  lineWidth?: string;
  lineHeight?: string;
  baseAngle?: number;
  className?: string;
  style?: React.CSSProperties;
}

export default function MagnetLines({
  rows = 9,
  columns = 9,
  containerSize = "60vmin", // Adjusted from original "80vmin" as per plan
  lineColor = "orange", // Adjusted to fit theme, e.g., "orange"
  lineWidth = "0.8vmin",
  lineHeight = "5vmin",
  baseAngle = -10, // Default from provided code
  className = "",
  style = {}
}: MagnetLinesProps) {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const items = Array.from(container.querySelectorAll("span"));

    const onPointerMove = (event: PointerEvent) => {
      const pointer = { x: event.clientX, y: event.clientY };
      items.forEach((item) => {
        const rect = item.getBoundingClientRect();
        const centerX = rect.x + rect.width / 2;
        const centerY = rect.y + rect.height / 2;

        const b = pointer.x - centerX;
        const a = pointer.y - centerY;
        const c = Math.sqrt(a * a + b * b) || 1;
        const r =
          (Math.acos(b / c) * 180) / Math.PI * (pointer.y > centerY ? 1 : -1);

        item.style.setProperty("--rotate", `${r}deg`);
      });
    };

    window.addEventListener("pointermove", onPointerMove);

    if (items.length) {
      const middleIndex = Math.floor(items.length / 2);
      if (items[middleIndex]) { // Check if items[middleIndex] exists
        const rect = items[middleIndex].getBoundingClientRect();
        // Initial pointer position can be tricky if component isn't fully centered
        // For now, let's use the center of the container for initial animation trigger
        if (containerRef.current) {
            const containerRect = containerRef.current.getBoundingClientRect();
            onPointerMove({
                clientX: containerRect.left + containerRect.width / 2,
                clientY: containerRect.top + containerRect.height / 2
            } as PointerEvent);
        }
      }
    }

    return () => {
      window.removeEventListener("pointermove", onPointerMove);
    };
  }, [rows, columns]); // Add dependencies rows, columns to re-run effect if they change

  const total = rows * columns;
  const spans = Array.from({ length: total }, (_, i) => (
    <span
      key={i}
      style={{
        // @ts-ignore
        "--rotate": `${baseAngle}deg`,
        backgroundColor: lineColor,
        width: lineWidth,
        height: lineHeight
      }}
    />
  ));

  return (
    <div
      ref={containerRef}
      className={`magnetLines-container ${className}`}
      style={{
        display: "grid",
        gridTemplateColumns: `repeat(${columns}, 1fr)`,
        gridTemplateRows: `repeat(${rows}, 1fr)`,
        width: containerSize,
        height: containerSize,
        ...style
      }}
    >
      {spans}
    </div>
  );
}
