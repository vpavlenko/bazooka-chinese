type Frequency = [string, number];

export type CharacterArray = {
  t: string;
  w: string;
}[];

type Translation =
  | ["translation_word", CharacterArray]
  | ["punctuation", string];

type Line = {
  chinese_source: string;
  english_source: string;
  translation: Translation[];
};

export type Chapter = {
  frequencies: Frequency[];
  lines: Line[];
};
