# K2 Curriculum Expansion Plan: Advanced Activity Variants

## Executive Summary
This plan introduces **5 new Sheet 1 (S1) activities** and **2 new Sheet 2 (S2) activities** to the K2 Phonics Curriculum. These activities are designed to progressively increase in difficulty, moving from basic recognition to spelling, logic, and reading comprehension.

The implementation will require updating `universal_factory.py` to support "Activity Modes" and expanding the `project_state.json` (or a sidebar configuration) to include Riddle data.

---

## 1. The New Activity Menu

### Sheet 1 (S1) Variants: Cognitive & Writing
These activities replace the standard "Trace/Circle/Match" panels (A, B, C) for specific lessons.

| Type | Activity Name | Panel Components | Skill Focus | Complexity |
| :--- | :--- | :--- | :--- | :--- |
| **S1-A** | **The Starter** | **Fill-in Consonants**<br>Display `_at`, `_an`, etc. Student writes 'b', 'c', 'r'. | Phonics (Onsets) | Low |
| **S1-B** | **The Scrambler** | **Unscramble**<br>Icon + Scrambled text (`t a c`) + Writing Line. | Spelling | High |
| **S1-C** | **The Selector** | **Circle Correct Icon**<br>Word is shown. Two icons displayed (Target vs Distractor). | Reading | Low |
| **S1-D** | **The Logician** | **Odd One Out**<br>3 Icons shown: 2 from Family, 1 Distractor. Circle the one that doesn't belong. | Rhyming Logic | Medium |
| **S1-E** | **The Creator** | **Mini Grid + Draw**<br>Panel A/B: 4x4 Letter Grid (Find Word). Panel C: "Read & Draw" (Empty box). | Recognition + Arts | High |

### Sheet 2 (S2) Variants: Interactive Application
These activities replace the standard "Sort & Glue" panels (D, E).

| Type | Activity Name | Panel Components | Skill Focus | Complexity |
| :--- | :--- | :--- | :--- | :--- |
| **S2-A** | **The Riddle Search** | **Panel D: Word Riddles**<br>Text clues (e.g., "I fly at night").<br>**Panel E: Big Word Search**<br>10x10 Grid containing the answers. | Reading Comp. | Very High |
| **S2-B** | **The Rhyme Hunter** | **Panel D: Icon Scatter**<br>10-12 Mixed Icons (Target + Distractors) scattered.<br>**Panel E: Checklist**<br>"Find 3 -at words", "Square rhymes", "Underline target". | Visual Scanning | Medium |

---

## 2. Curriculum Map (Q01 - Q29)

We will use a **Spiral Progression**, introducing simpler activities first and cycling in complex ones as students gain confidence.

#### Phase 1: Foundations (Short Vowel A) - *Focus: Recognition*
*High frequency of standard Tracing and Icon Selection.*

| Lesson | Family | S1 Activity | S2 Activity | Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **Q01** | -at | **Classic** (Trace/Match) | **Classic** (Sort/Glue) | Establish baseline. |
| **Q02** | -an | **Classic** (Trace/Match) | **Classic** (Sort/Glue) | Reinforce baseline. |
| **Q03** | -ap | **S1-C: The Selector** | **S2-B: Rhyme Hunter** | Intro to visual discrimination. |
| **Q04** | -ag | **S1-A: The Starter** | **Classic** (Sort/Glue) | Intro to writing initial sounds. |
| **Q05** | -am | **S1-D: The Logician** | **S2-B: Rhyme Hunter** | Intro to rhyming logic. |
| **Q06** | -ad | **Classic** (Trace/Match) | **Classic** (Sort/Glue) | Review. |

#### Phase 2: Building Blocks (Short E & I) - *Focus: Spelling*
*Introducing Unscrambling and writing.*

| Lesson | Family | S1 Activity | S2 Activity | Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **Q07** | -et | **S1-A: The Starter** | **Classic** (Sort/Glue) | Focus on 'e' sound onset. |
| **Q08** | -en | **S1-B: The Scrambler** | **Classic** (Sort/Glue) | First spelling challenge. |
| **Q09** | -ed | **S1-C: The Selector** | **S2-B: Rhyme Hunter** | Visual refresher. |
| **Q10** | -it | **S1-E: The Creator** | **Classic** (Sort/Glue) | Intro to Read & Draw. |
| **Q11** | -in | **S1-B: The Scrambler** | **S2-B: Rhyme Hunter** | Spelling + Searching. |
| **Q12** | -ig | **S1-D: The Logician** | **Classic** (Sort/Glue) | Logic check. |

#### Phase 3: Patterns (Short O & U) - *Focus: Logic*
*Heavy use of Odd One Out and Grid searches.*

| Lesson | Family | S1 Activity | S2 Activity | Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **Q13** | -ip | **S1-D: The Logician** | **S2-A: Riddle Search** | First Riddle usage (Challenge). |
| **Q14** | -ot | **S1-E: The Creator** | **Classic** (Sort/Glue) | Drawing. |
| **Q15** | -og | **S1-C: The Selector** | **S2-B: Rhyme Hunter** | Standard visual search. |
| **Q16** | -op | **S1-A: The Starter** | **S2-A: Riddle Search** | Consonant check + Riddles. |
| **Q17** | -ox | **Classic** (Trace/Match) | **Classic** (Sort/Glue) | Rest/Review. |
| **Q18** | -ug | **S1-B: The Scrambler** | **S2-B: Rhyme Hunter** | Spelling check. |

#### Phase 4: Mastery (Mixed Families) - *Focus: Comprehension*
*Complex mixes of all activities.*

| Lesson | Family | S1 Activity | S2 Activity | Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **Q19** | -un | **S1-E: The Creator** | **S2-A: Riddle Search** | High creativity. |
| **Q20** | -ut | **S1-D: The Logician** | **S2-B: Rhyme Hunter** | Logic intensive. |
| **Q21** | -ub | **S1-B: The Scrambler** | **Classic** (Sort/Glue) | Spelling. |
| **Q22** | -ob | **S1-C: The Selector** | **S2-A: Riddle Search** | Reading vs Riddles. |
| **Q23** | -id | **Classic** (Trace/Match) | **Classic** (Sort/Glue) | Review. |

#### Phase 5: The Extended Set (Q24-Q29) - *Focus: Challenge*

| Lesson | Family | S1 Activity | S2 Activity | Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **Q24** | -ab | **S1-E: The Creator** | **S2-B: Rhyme Hunter** | Draw + Hunt. |
| **Q25** | -eg | **S1-B: The Scrambler** | **Classic** (Sort/Glue) | Spelling. |
| **Q26** | -ib | **S1-D: The Logician** | **S2-A: Riddle Search** | Logic + Riddles. |
| **Q27** | -ix | **S1-A: The Start** | **S2-B: Rhyme Hunter** | 'x' ending focus. |
| **Q28** | -od | **S1-C: The Selector** | **Classic** (Sort/Glue) | Visual check. |
| **Q29** | -um | **S1-E: The Creator** | **S2-A: Riddle Search** | Final Boss: Draw & Riddle. |

---

## 3. Implementation Requirements

### 3.1 Data Gaps
To enable **S2-A (Word Riddle)**, we need a data source for riddles.
*   **Action:** Create `data/riddles.json` mapping words ("cat") to simple clues ("I say Meow").
*   *Fallback:* If no riddle exists for a word, the factory will fallback to "Word Definitions" or simply "Read and Find [WORD]".

### 3.2 Code Updates
1.  **Modify `universal_factory.py`**:
    *   Add `generate_sheet_1_variant(quest, variant_type)`
    *   Add `generate_sheet_2_variant(quest, variant_type)`
    *   Implement Grid Generation algorithm (for Word Search & Mini Grid).
    *   Implement Icon Scattter algorithm (for Rhyme Hunter - ensure no overlap).

2.  **Configuration**:
    *   Define the `CURRICULUM_MAP` dictionary in Python to strictly assign these variants to the Quest IDs as planned above.
