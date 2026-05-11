# QuaQua
# Quest of Knowledge & Tactile Foundation (Level 1 Adventure Bundle)

## About the Project
**Quest of Knowledge** and the **Tactile Foundation** series constitute an automated, high-velocity interactive curriculum designed for Kindergarten to 2nd Grade (K-2) students and their parents. The project shifts away from traditional linear testing by employing a **Non-Linear Quest Map**, allowing children to navigate a branching adventure of 25 Quests that converge at key educational milestones. The ultimate goal is to journey from the *Garden Gate* to the *Throne Room* to earn an Achievement Certificate from the Strawberry King.

## Curriculum Architecture
The curriculum is strictly mapped to Common Core (CCSS) standards and is divided into two primary academic pillars:

*   **Literacy & Language (Phonemic Awareness):** Focuses on sound recognition and independent reading/writing. Topics include rhyming skills, initial and middle sound isolation, short vowels (A, E, I, O, U), and CVC (Consonant-Vowel-Consonant) word construction. 
*   **Mathematics & Number Sense:** Prioritizes visual and tactile logic over abstract equations. Core topics include visual subitizing (instantly recognizing quantities), part-part-whole relationships, ten-frame addition, and number line navigation.

## Technical Generation & Automation
The project utilizes an **Autonomous Worksheet Publishing & Promotion System** running on the agent-first **Google Anti-gravity IDE**. 

*   **Agentic Pipeline:** Specialized AI agents (like the *CurriculumArchitect*, *Visual_Architect_v1*, and *Visual_QA_Supervisor*) automatically process JSON curriculum specs, perform semantic/instance segmentation to extract clean overlapping visual assets, and enforce rigorous pedagogical logic.
*   **Backend Rendering:** Math and logic assets are built using LaTeX and TikZ for pristine vector generation. Phonics and visual layouts use Python scripts (like `batch_generate_visuals.py`) alongside Pillow to procedurally overlay text and graphics onto pre-designed template bases. 
*   **Visual Logic:** The agents abandon static rectangular bounds for dynamic SVG/Canvas-based object placement, ensuring visual hierarchy and proper developmental spacing (e.g., Fitts's Law considerations for fine motor skills).

## Worksheet Design & "Safe Zone" Standards
Every Quest module generates a **3-page Storybook Worksheet** and **6 Mastery Flashcards**. To eliminate visual clutter and cognitive overload, all output adheres to rigid formatting constraints:

*   **The Safe Zone:** All academic tasks and text are strictly locked to the top-left quadrant of an A4 landscape sheet on a 100% pure white background.
*   **Creative Canvas:** The remaining L-shaped space is left blank for the child to manually draw their adventure path and connect the quests.
*   **Typography:** The **Lexend font at 24pt** is mandated for maximum readability for early learners.
*   **Tactile Math Standard:** All generated number lines must feature a strict **1.0 cm horizontal gap** between digits so small fingers can track their "hops" accurately.
*   **Art Style:** Only high-contrast, 2D stylized flat icons are used—realistic or photographic elements are prohibited to prevent visual noise.

## Lesson & Assessment Framework (Vortex Pedagogy)
The curriculum empowers parents to act as "Adventure Guides" using the **Standardized Bento Lesson Template** system. Each lesson requires no prior teaching experience and takes 30 minutes to complete.

*   **The 3-2-1 Phonics Strategy:** Language worksheets progress smoothly from Introduction (Tracing, Circling, Matching), to Practice (Sorting and cut-outs), and culminate in a manual Mastery board game.
*   **Observational Band Grading (IELTS-style):** Parents assess the child's progress via the 6-card Mastery Flashcard sets using an observational 1-5 Band Scale. 
    *   **Band 4-5 (Mastery):** The child answers in under 2 seconds without assistance and moves forward on the map.
    *   **Band 1-2 (Novice):** The child requires heavy prompting or is guessing, triggering a "Practice Loop" for 5 minutes a day before advancing.
