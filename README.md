# QuaQua
Kindy Quest: Automated Curriculum Publishing Engine
About the Project
Kindy Quest (featuring the Quest of Knowledge and Tactile Foundation series) is an autonomous, high-velocity publishing system designed to generate professional-grade, interactive curricula for Kindergarten to 2nd Grade (K-2) students.

The project shifts away from traditional linear testing by employing a Non-Linear Quest Map. Children navigate a branching adventure of 29 Quests that converge at key educational milestones. The ultimate goal is to journey from the Garden Gate to the Throne Room to earn an Achievement Certificate from the Strawberry King.

Commercial Objective
The primary directive of this repository is to generate, format, and package high-quality educational worksheet bundles for commercial sale on digital storefronts and e-commerce platforms. The pipeline must operate autonomously, taking structured data inputs and outputting storefront-ready digital packages.

1. Curriculum Architecture
The curriculum is strictly mapped to Common Core (CCSS) standards and is divided into two primary academic pillars:

Literacy & Language (Phonemic Awareness): Focuses on sound recognition and independent reading/writing. Topics include rhyming skills, initial and middle sound isolation, short vowels (A, E, I, O, U), and CVC (Consonant-Vowel-Consonant) word construction.

Mathematics & Number Sense: Prioritizes visual and tactile logic over abstract equations. Core topics include visual subitizing (instantly recognizing quantities), part-part-whole relationships, ten-frame addition, and number line navigation.

2. Lesson & Assessment Framework (Vortex Pedagogy)
The curriculum empowers parents to act as "Adventure Guides" using a Standardized Bento Lesson Template system. Each lesson requires no prior teaching experience and takes 30 minutes to complete.

The 3-2-1 Phonics Strategy: Language worksheets progress smoothly from Introduction (Tracing, Circling, Matching), to Practice (Sorting and cut-outs), and culminate in a manual Mastery board game.

Observational Band Grading (IELTS-style): Parents assess the child's progress via 6-card Mastery Flashcard sets using an observational 1-5 Band Scale.

Band 4-5 (Mastery): The child answers in under 2 seconds without assistance and moves forward on the map.

Band 1-2 (Novice): The child requires heavy prompting or is guessing, triggering a "Practice Loop" for 5 minutes a day before advancing.

3. Technical Generation & Automation
The project utilizes an Autonomous Worksheet Publishing System running on the agent-first Google Anti-gravity IDE.

Agentic Pipeline: Specialized AI agents (such as CurriculumArchitect, Visual_Architect_v1, and Visual_QA_Supervisor) automatically process JSON curriculum specs, perform semantic/instance segmentation to extract clean visual assets, and enforce rigorous pedagogical logic.

Backend Rendering: Math and logic assets are built using LaTeX and TikZ for pristine vector generation. Phonics and visual layouts use Python scripts (FastAPI/React orchestration) alongside Pillow to procedurally overlay text and graphics onto pre-designed template bases.

Commercial Packaging: The pipeline must automatically group the generated 3-page Storybook Worksheets and 6 Mastery Flashcards into compiled, organized directories (or .zip files) ready for digital distribution.

4. Worksheet Design & "Safe Zone" Standards
Every Quest module generates a 3-page Storybook Worksheet and 6 Mastery Flashcards. To eliminate visual clutter and cognitive overload, all output must adhere to rigid formatting constraints:

The Safe Zone: All academic tasks and text are strictly locked to the top-left quadrant of an A4 landscape sheet on a 100% pure white background.

Creative Canvas: The remaining L-shaped space is left blank for the child to manually draw their adventure path and connect the quests.

Typography: The Lexend font at 24pt is mandated for maximum readability for early learners.

Tactile Math Standard: All generated number lines must feature a strict 1.0 cm horizontal gap between digits so small fingers can track their "hops" accurately.

Structural Consistency: Panel layouts utilize a shortened height for Panel C to ensure fit across varying template designs, maintaining consistent green borders around the panels.

Localization Strictness: The curriculum targets specific linguistic needs. Generated text must rely exclusively on White Hmong words and standard number symbols. The inclusion of Thai script or Thai numbers is strictly prohibited across all counting posters and worksheets.

Art Style: Only high-contrast, 2D stylized flat icons are used. Realistic or photographic elements are explicitly prohibited to prevent visual noise.

5. System Error & Feedback Protocols
When refining or interacting with the generation pipeline and AI agents, the following system-level protocol applies:

Negative Feedback Loop: To ensure the Visual_QA_Supervisor and generation agents understand correction data without ambiguity, all process failures, formatting violations, or visual errors must be explicitly labeled in the system as "mistakes".

Art Style: Only high-contrast, 2D stylized flat icons are used. Realistic or photographic elements are explicitly prohibited to prevent visual noise.

5. System Error & Feedback Protocols
When refining or interacting with the generation pipeline and AI agents, the following system-level protocol applies:

Negative Feedback Loop: To ensure the Visual_QA_Supervisor and generation agents understand correction data without ambiguity, all process failures, formatting violations, or visual errors must be explicitly labeled in the system as "mistakes".
