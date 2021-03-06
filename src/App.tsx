import React, { useState, useEffect } from "react";
import styled from "styled-components";
import { Tooltip, Button, Input } from "antd";
import "./App.css";
import { CHAPTER } from "./chapter_1_translated";
import { CharacterArray } from "./types";

const CURRENT_CHAPTER = CHAPTER;

const PaddedDiv = styled.div`
  margin-top: 1em;
`;

function usePersistedState(key: string, defaultValue: any) {
  const [state, setState] = useState(() => {
    return JSON.parse(
      localStorage.getItem(key) || JSON.stringify(defaultValue)
    );
  });
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
  const [wordsToSkip, setWordsToSkip] = useState<string[]>([]);
  let newWordToAsk = "";
  let newWordFrequency = 0;
  const [manualKnownWord, setManualKnownWord] = useState("");

  CURRENT_CHAPTER.frequencies.forEach(({ word, frequency }, index) => {
    if (
      knownWords.indexOf(word) === -1 &&
      wordsToLearnNow.indexOf(word) === -1 &&
      wordsToSkip.indexOf(word) === -1 &&
      newWordToAsk === ""
    ) {
      newWordToAsk = word;
      newWordFrequency = frequency;
    }
  });

  return (
    <div>
      <div style={{ position: "fixed", right: 0 }}>
        <Input
          style={{ width: "20em" }}
          placeholder="Add word to known words"
          value={manualKnownWord}
          onChange={event => setManualKnownWord(event.target.value)}
          onPressEnter={() => {
            setKnownWords(knownWords.concat([manualKnownWord]));
            setManualKnownWord("");
          }}
        />
      </div>
      <div
        style={{
          paddingBottom: "2em",
          backgroundColor: "white"
        }}
      >
        <div>
          Known words:{" "}
          <span style={{ color: "green" }}>
            {knownWords.map(word => word + ", ")}
          </span>
        </div>
        <div>
          Words to learn now:{" "}
          <span style={{ color: "blue" }}>
            {wordsToLearnNow.map(word => word + ", ")}
          </span>
        </div>
        <div>
          The word <b>{newWordToAsk}</b> has <b>{newWordFrequency}</b>{" "}
          occurrences in this chapter.
        </div>

        <div>
          <Button
            onClick={() => setKnownWords(knownWords.concat([newWordToAsk]))}
          >
            I know it
          </Button>{" "}
          <Button
            onClick={() =>
              setWordsToLearnNow(wordsToLearnNow.concat([newWordToAsk]))
            }
          >
            Let's learn it
          </Button>{" "}
          <Button
            onClick={() => setWordsToSkip(wordsToSkip.concat([newWordToAsk]))}
          >
            Skip it
          </Button>
        </div>
      </div>

      <div style={{ margin: "2em", width: "700px" }}>
        {CURRENT_CHAPTER.lines.map(line => {
          return (
            <div key={line.chinese_source}>
              <PaddedDiv>{line.chinese_source.split(' ').join('')}</PaddedDiv>
              <PaddedDiv>
                {line.translation.map(([token_type, token_list]) => {
                  if (token_type === "punctuation") {
                    return <span>{token_list} </span>;
                  } else if (token_type === "translation_word") {
                    return (token_list as CharacterArray).map(({ t, w }) => {
                      return (
                        <Tooltip title={t}>
                          <span
                            style={{
                              color:
                                knownWords.indexOf(w) !== -1
                                  ? "green"
                                  : wordsToLearnNow.indexOf(w) !== -1
                                  ? "blue"
                                  : "red"
                            }}
                          >
                            {w}{" "}
                          </span>
                        </Tooltip>
                      );
                    });
                  }
                })}
                ˝
              </PaddedDiv>
              <PaddedDiv>
                {line.translation.map(
                  ([token_type, token_list, alignment_word]) => {
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
                            {alignment_word ? (
                              <span style={{ color: "black" }}>
                                {alignment_word}
                              </span>
                            ) : (
                              <span style={{ color: "gray" }}>{t}</span>
                            )}{" "}
                          </Tooltip>
                        );
                      });
                    }
                  }
                )}
                ˝
              </PaddedDiv>
              <PaddedDiv
                dangerouslySetInnerHTML={{ __html: line.english_source }}
              ></PaddedDiv>
              <hr />
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default App;
