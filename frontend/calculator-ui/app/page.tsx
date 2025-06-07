"use client";

import MagnetLines from "@/components/MagnetLines";
import Display from "@/components/Display";
import Button from "@/components/Button";
import { useState } from 'react';

const mainButtons = [
  { label: "AC", type: "action", value: "clear" },
  { label: "+/-", type: "action", value: "negate" },
  { label: "%", type: "action", value: "percent" },
  { label: "÷", type: "operator", value: "/" },

  { label: "7", type: "number", value: "7" },
  { label: "8", type: "number", value: "8" },
  { label: "9", type: "number", value: "9" },
  { label: "×", type: "operator", value: "*" },

  { label: "4", type: "number", value: "4" },
  { label: "5", type: "number", value: "5" },
  { label: "6", type: "number", value: "6" },
  { label: "-", type: "operator", value: "-" },

  { label: "1", type: "number", value: "1" },
  { label: "2", type: "number", value: "2" },
  { label: "3", type: "number", value: "3" },
  { label: "+", type: "operator", value: "+" },

  { label: "0", type: "number", value: "0", gridSpan: 2 },
  { label: ".", type: "number", value: "." },
  { label: "=", type: "operator", value: "equals" },
];

const scientificButtons = [
  { label: "xʸ", type: "scientific", value: "power" },
  { label: "√", type: "scientific", value: "sqrt" },
  { label: "ln", type: "scientific", value: "ln" },
  { label: "log₁₀", type: "scientific", value: "log10" },
  { label: "π", type: "scientific", value: "pi" },
  { label: "sin", type: "scientific", value: "sin" },
  { label: "cos", type: "scientific", value: "cos" },
  { label: "tan", type: "scientific", value: "tan" },
  { label: "1/x", type: "scientific", value: "reciprocal" },
];

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

export default function HomePage() {
  const [currentOperand, setCurrentOperand] = useState("0");
  const [previousOperand, setPreviousOperand] = useState<string | null>(null);
  const [operation, setOperation] = useState<string | null>(null);
  const [expression, setExpression] = useState("");
  const [overwrite, setOverwrite] = useState(true);

  const formatOperand = (operand: string | null) => {
    if (operand === null || operand === "null" || operand === "undefined") return "";
    return operand;
  };

  const displayedValue = formatOperand(currentOperand);
  const displayedExpression = expression.replace(/null|undefined/g, "");

  const clear = () => {
    setCurrentOperand("0");
    setPreviousOperand(null);
    setOperation(null);
    setExpression("");
    setOverwrite(true);
  };

  const appendNumber = (number: string) => {
    if (number === "." && currentOperand.includes(".")) return;

    let newCurrentOperand;
    if (overwrite) {
      newCurrentOperand = number;
      setOverwrite(false);
    } else {
      if (currentOperand.length > 15 && number !== ".") return;
      newCurrentOperand = (currentOperand === "0" && number !== ".") ? number : currentOperand + number;
    }
    setCurrentOperand(newCurrentOperand);

    if (overwrite) {
        if (previousOperand && operation) {
            setExpression(`${formatOperand(previousOperand)} ${operation} ${newCurrentOperand}`);
        } else {
            setExpression(newCurrentOperand);
        }
    } else {
        setExpression(prev => prev + number);
    }
  };

  const chooseOperation = (op: string) => {
    if (currentOperand === "" && previousOperand === null) {
        if (op === '-' || op === '+') {
            setPreviousOperand("0");
            setOperation(op);
            setExpression(`0 ${op} `);
            setCurrentOperand("");
            setOverwrite(false);
        }
        return;
    }

    if (currentOperand === "" && previousOperand !== null) {
        setOperation(op);
        setExpression(`${formatOperand(previousOperand)} ${op} `);
        return;
    }

    if (previousOperand !== null && operation && currentOperand !== "" && !overwrite) {
        // This implies a sequence like "A op1 B op2". We should calculate "A op1 B" first.
        // The `calculate` function will update `currentOperand` with the result.
        // Then, that result becomes `previousOperand` for the new operation `op`.
        // This relies on `calculate` correctly setting `currentOperand` and `overwrite`.
        // And `calculate` itself uses `operation`, `previousOperand`, `currentOperand` from state.
        // This is a tricky sequence with async `calculate`.
        // A simplified model: call calculate, then use its result (now in currentOperand)
        // to set up the next operation.

        // Store state that calculate() will modify, to correctly form new expression
        const pOp = previousOperand;
        const cOp = currentOperand;
        const curOperation = operation;

        calculate(); // This will update currentOperand to result, clear operation, clear previousOperand, set overwrite.

        // After calculate(), currentOperand holds the result.
        // We want: result newOp ...
        setPreviousOperand(currentOperand); // Result becomes previous for the new operation
        setOperation(op);
        setExpression(`${formatOperand(currentOperand)} ${op} `); // Expression starts with result + new op
        setCurrentOperand("");
        setOverwrite(true); // Ready for next number
        return;
    }

    // Standard path: currentOperand is a number, or it's a result (overwrite is true)
    if (currentOperand !== "") {
        setPreviousOperand(currentOperand);
    }
    setOperation(op);
    const exprBase = currentOperand !== "" ? formatOperand(currentOperand) : (previousOperand ? formatOperand(previousOperand) : "");
    setExpression(`${exprBase} ${op} `);
    setCurrentOperand("");
    setOverwrite(true);
  };

  async function fetchCalculation(endpoint: string, params: Record<string, string>) {
    const query = new URLSearchParams(params).toString();
    try {
      const response = await fetch(`${API_BASE_URL}/${endpoint}?${query}`);
      if (!response.ok) {
        const data = await response.json().catch(() => ({ detail: "API error, invalid JSON" }));
        throw new Error(data.detail || `API Error ${response.status}`);
      }
      const data = await response.json();
      if (data.result === undefined) {
        throw new Error("API Error: 'result' missing");
      }
      return data.result;
    } catch (error: any) {
      console.error("API Call failed:", error);
      setCurrentOperand(error.message || "Error from API");
      setOverwrite(true);
      return "Error";
    }
  }

  const calculate = async () => {
    let P = previousOperand;
    let C = currentOperand;
    const O = operation; // Capture operation at time of calling calculate

    if (!O || P === null) return;

    if (C === "" && P !== null) { // Handle "A op =" case by using P as C
        C = P;
    }

    const prevNum = parseFloat(P);
    const currNum = parseFloat(C);

    if (isNaN(prevNum) || isNaN(currNum)) {
      setCurrentOperand("Error: Invalid Number");
      setOverwrite(true);
      return;
    }

    let result: string | number = "Error";
    let endpoint = "";
    let apiParams: Record<string, string> = {};

    switch (O) { // Use captured operation 'O'
        case "+": endpoint = "add"; apiParams = { x: prevNum.toString(), y: currNum.toString() }; break;
        case "-": endpoint = "subtract"; apiParams = { x: prevNum.toString(), y: currNum.toString() }; break;
        case "*": endpoint = "multiply"; apiParams = { x: prevNum.toString(), y: currNum.toString() }; break;
        case "/": endpoint = "divide"; apiParams = { x: prevNum.toString(), y: currNum.toString() }; break;
        case "power": endpoint = "power"; apiParams = { base: prevNum.toString(), exponent: currNum.toString() }; break;
        default: setCurrentOperand("Error: Unknown Op"); setOverwrite(true); return;
    }

    result = await fetchCalculation(endpoint, apiParams);

    if (String(result) !== "Error") {
      setExpression(`${formatOperand(P)} ${O} ${formatOperand(C)} = ${String(result)}`);
      setCurrentOperand(String(result));
    }

    setOperation(null);
    setPreviousOperand(null);
    setOverwrite(true);
  };

  const handleScientific = async (sciOp: string) => {
    let inputVal = currentOperand;
    let exprDisplayVal = formatOperand(currentOperand);

    if (sciOp !== "pi") {
        if ((inputVal === "" || (inputVal === "0" && overwrite)) && previousOperand !== null && operation === null) {
            inputVal = previousOperand;
            exprDisplayVal = formatOperand(previousOperand);
        } else if (inputVal === "") {
            inputVal = "0";
            exprDisplayVal = "0";
        }

        if (isNaN(parseFloat(inputVal))) {
            setCurrentOperand("Error: Invalid Input");
            setOverwrite(true);
            return;
        }
    }

    let result: string | number = "Error";
    let endpoint = "";
    let apiParams: Record<string, string> = {};
    const opSymbol = scientificButtons.find(b => b.value === sciOp)?.label || sciOp;
    let finalExpression = "";

    switch (sciOp) {
        case "sqrt": endpoint = "sqrt"; apiParams = { number: inputVal }; finalExpression = `${opSymbol}(${exprDisplayVal})`; break;
        case "ln": endpoint = "ln"; apiParams = { number: inputVal }; finalExpression = `${opSymbol}(${exprDisplayVal})`; break;
        case "log10": endpoint = "log10"; apiParams = { number: inputVal }; finalExpression = `${opSymbol}(${exprDisplayVal})`; break;
        case "sin": endpoint = "sine"; apiParams = { angle: inputVal }; finalExpression = `${opSymbol}(${exprDisplayVal})`; break;
        case "cos": endpoint = "cosine"; apiParams = { angle: inputVal }; finalExpression = `${opSymbol}(${exprDisplayVal})`; break;
        case "tan": endpoint = "tangent"; apiParams = { angle: inputVal }; finalExpression = `${opSymbol}(${exprDisplayVal})`; break;
        case "reciprocal": endpoint = "reciprocal"; apiParams = { number: inputVal }; finalExpression = `1/(${exprDisplayVal})`; break;
        case "pi": endpoint = "pi"; apiParams = {}; break;
        default: setCurrentOperand("Error: Unknown SciOp"); setOverwrite(true); return;
    }

    result = await fetchCalculation(endpoint, apiParams);

    if (String(result) !== "Error") {
        if (sciOp === "pi") {
            const currentExpression = expression; // Use state 'expression'
            const newExpression = (currentExpression === "" || currentExpression.trim().match(/[\+\-\×\÷]$/) || overwrite)
                                  ? currentExpression + String(result)
                                  : String(result);
            setExpression(newExpression);
            setCurrentOperand(String(result));
            setOverwrite(false);
        } else {
            setExpression(`${finalExpression} = ${String(result)}`);
            setCurrentOperand(String(result));
            setOverwrite(true);
        }
    }
  };

  const negate = () => {
    if (currentOperand === "Error" || isNaN(parseFloat(currentOperand))) return;
    const val = parseFloat(currentOperand) * -1;
    const strVal = val.toString();
    setCurrentOperand(strVal);

    setExpression(prev => {
        if (prev.endsWith(currentOperand)) {
            return prev.substring(0, prev.length - currentOperand.length) + strVal;
        } else if (currentOperand === "0" && (prev === "0" || prev === "")) {
            return strVal;
        }
        return prev ? `${prev} ${strVal}` : strVal; // Fallback if currentOperand not directly in expression end
    });
    setOverwrite(false);
  };

  const percent = () => {
    if (currentOperand === "Error" || isNaN(parseFloat(currentOperand))) return;
    const val = parseFloat(currentOperand) / 100;
    const strVal = val.toString();

    setExpression(prev => {
        if (prev.endsWith(currentOperand)) {
             return prev.substring(0, prev.length - currentOperand.length) + `${currentOperand}% = ${strVal}`;
        }
        return `${currentOperand}% = ${strVal}`;
    });
    setCurrentOperand(strVal);
    setOverwrite(true);
  };

  const handleButtonClick = (value: string, type: string) => {
    if (type === 'number') {
      appendNumber(value);
    } else if (type === 'action') {
      if (value === 'clear') clear();
      else if (value === 'negate') negate();
      else if (value === 'percent') percent();
    } else if (type === 'operator') {
      if (value === 'equals') {
        calculate();
      } else {
        chooseOperation(value);
      }
    } else if (type === 'scientific') {
      if (value === 'power') {
        chooseOperation(value);
      } else {
        handleScientific(value);
      }
    }
  };

  return (
    <main className="relative flex flex-col items-center justify-center min-h-screen bg-[var(--color-background)] text-[var(--color-text-default)] overflow-hidden py-4">
      <div className="absolute inset-0 z-0">
        <MagnetLines
          rows={12}
          columns={12}
          containerSize="100vw"
          lineColor="var(--color-grey-light)"
          lineWidth="1px"
          lineHeight="4vmin"
          baseAngle={-15}
          style={{ margin: "0" }}
        />
      </div>
      <div className="relative z-10 flex flex-col items-center justify-center p-4 sm:p-6 md:p-8 bg-white/80 dark:bg-black/80 backdrop-blur-lg rounded-lg shadow-2xl w-full max-w-xs sm:max-w-sm md:max-w-md">
        <Display value={displayedValue} expression={displayedExpression} />
        <div className="grid grid-cols-5 gap-1 sm:gap-2 w-full mb-3">
          {scientificButtons.map((btn) => (
            <Button
              key={btn.value}
              label={btn.label}
              onClick={() => handleButtonClick(btn.value, btn.type)}
              type={btn.type as any}
            />
          ))}
          {Array.from({ length: (5 - scientificButtons.length % 5) % 5 }).map((_, i) => (
            <div key={`fill-sci-${i}`} className="aspect-square"></div>
          ))}
        </div>
        <div className="grid grid-cols-4 gap-1 sm:gap-2 w-full">
          {mainButtons.map((btn) => (
            <Button
              key={btn.value}
              label={btn.label}
              onClick={() => handleButtonClick(btn.value, btn.type)}
              type={btn.type as any}
              gridSpan={btn.gridSpan}
            />
          ))}
        </div>
      </div>
    </main>
  );
}
