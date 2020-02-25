import React, { useState, useEffect } from "react";
import styled from "styled-components";
import { Tooltip, Button } from "antd";
import "./App.css";
import { CHAPTER } from "./chapter_1_translated";
import { CharacterArray } from "./types";

const CURRENT_CHAPTER = CHAPTER;

const PaddedDiv = styled.div`
  margin-top: 1em;
`;

function usePersistedState(key: string, defaultValue: any) {
  const [state, setState] = useState(
    () => {
      return JSON.parse(
        localStorage.getItem(key) || JSON.stringify(defaultValue)
      );
    }
    // () => []
  );
  useEffect(() => {
    localStorage.setItem(key, JSON.stringify(state));
  }, [key, state]);
  return [state, setState];
}

function App() {
  const [knownWords, setKnownWords] = usePersistedState("knownWords", []) as [
    string[],
    (newValue: string[]) => void
  ];
  const [wordsToLearnNow, setWordsToLearnNow] = usePersistedState(
    "wordsToLearnNow",
    []
  ) as [string[], (newValue: string[]) => void];
  let newWordToAsk = "";

  CURRENT_CHAPTER.frequencies.forEach(([word], index) => {
    if (knownWords.indexOf(word) === -1) {
      if (wordsToLearnNow.indexOf(word) === -1) {
        if (newWordToAsk === "") {
          newWordToAsk = word;
        }
      }
    }
  });

  return (
    <div>
      <div>
        Known words:{" "}
        <span style={{ color: "green" }}>
          {knownWords.map(word => word + ", ")}
        </span>
      </div>
      <div>
        Words to learn now:{" "}
        <span style={{ color: "blue" }}>{wordsToLearnNow.map(word => word + ", ")}</span>
      </div>
      <div>
        Do you know the word <b>{newWordToAsk}</b>?
      </div>
      <div>
        <Button
          onClick={() => setKnownWords(knownWords.concat([newWordToAsk]))}
        >
          Yes
        </Button>{" "}
        <Button
          onClick={() =>
            setWordsToLearnNow(wordsToLearnNow.concat([newWordToAsk]))
          }
        >
          No
        </Button>
      </div>
      <div style={{ margin: "2em", width: "700px" }}>
        {CURRENT_CHAPTER.lines.map(line => {
          return (
            <>
              <PaddedDiv>{line.chinese_source}</PaddedDiv>
              <PaddedDiv>
                {line.translation.map(([token_type, token_list]) => {
                  if (token_type === "punctuation") {
                    return <span>{token_list} </span>;
                  } else if (token_type === "translation_word") {
                    return (token_list as CharacterArray).map(({ t, w }) => {
                      if (
                        knownWords.indexOf(w) !== -1 ||
                        wordsToLearnNow.indexOf(w) !== -1
                      ) {
                        return (
                          <Tooltip title={t}>
                            <span
                              style={{
                                color:
                                  knownWords.indexOf(w) !== -1
                                    ? "green"
                                    : "blue"
                              }}
                            >
                              {w}{" "}
                            </span>
                          </Tooltip>
                        );
                      }
                      return (
                        <Tooltip title={w}>
                          <span>{t} </span>
                        </Tooltip>
                      );
                    });
                  }
                })}
                ˝
              </PaddedDiv>
              <PaddedDiv
                dangerouslySetInnerHTML={{ __html: line.english_source }}
              ></PaddedDiv>
              <hr />
            </>
          );
        })}
      </div>
    </div>
  );
}

export default App;
