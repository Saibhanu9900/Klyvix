# Elite Terminal Frontend Design Specification

## 1. Overall Vision: Professional, Sleek, and High-End

The goal is to implement a frontend that embodies an "Elite Terminal" aesthetic, combining the professional polish of modern developer tools (e.g., Vercel, Linear) with the structured utility of a terminal interface. The design should be clean, high-contrast, and minimalist, focusing on clarity and functionality without radiant colors or heavy visual effects. It should feel premium and high-production-value, simple to understand, and efficient to use.

## 2. Layout Structure

The interface will consist of three primary regions:

*   **Left Sidebar (Navigation)**: A persistent, thin sidebar dedicated to primary navigation, including persona selection and other potential system links.
*   **Main Content Area**: The central and largest part of the screen, where all interactions, chat outputs, and structured results will be displayed.
*   **Input Bar**: A sleek, subtle input area at the bottom of the main content area for user commands and messages.

## 3. Color Palette

*   **Background**: Deep charcoal or obsidian (`#1A1A1A` or similar dark gray).
*   **Primary Text**: Crisp white (`#FFFFFF`).
*   **Secondary Text/Subtle Elements**: Light gray (`#AAAAAA`).
*   **Accent Colors**: A very subtle, muted green for success indicators (`#6EE7B7`) and a muted red for error/critical indicators (`#FCA5A5`). These should be used sparingly and only for functional emphasis.

## 4. Typography

*   **Primary Font (Content)**: A clean, highly legible sans-serif font (e.g., Inter, Lato) for general text, chat messages, and descriptions.
*   **Monospace Font (Code/Data/Headers)**: A premium monospace font (e.g., JetBrains Mono, Fira Code, SF Mono) for code blocks, structured data, system messages, and potentially section headers to reinforce the terminal aesthetic.
*   **Font Sizing**: Use a hierarchical sizing system to ensure readability and clear information architecture.

## 5. Component Details

### 5.1. Left Sidebar (Navigation)

*   **Structure**: A thin, fixed sidebar on the left side of the screen. It should be visually distinct but not intrusive, using the background color with a subtle 1px border on its right edge.
*   **Content**: This sidebar will house the persona selection (Study Mentor, Code Reviewer, Document Analyzer, Resume Reviewer, Research Assistant) and potentially other top-level navigation items (e.g., Dashboard, Settings, Logs, etc., if applicable to the project).
*   **Persona Display**: Each persona should be represented by a simple icon and its name. The active persona should have a clear, subtle highlight (e.g., a thin accent line or a slightly lighter background on hover/active state).
*   **Interaction**: Clicking a persona icon/name will switch the main content area to that persona's view.

### 5.2. Main Content Area (Chat/Output)

*   **General Display**: This area will display the conversation flow. Messages should appear as clean text blocks, without chat bubbles or avatars, maintaining a minimalist aesthetic.
*   **Streaming**: LLM responses should stream in progressively, appending tokens to the UI in real-time.
*   **Structured Output (e.g., Code Reviewer, Resume Reviewer)**:
    *   Instead of complex dashboards, structured results will be presented as **integrated, minimalist code-style blocks** within the main content stream.
    *   Use clear, text-based headings and subheadings (e.g., `## Summary`, `### Key Findings`).
    *   Tables (for issues, suggestions) should use simple ASCII-style borders or thin 1px solid lines for separation, ensuring readability without visual clutter.
    *   Severity indicators (Critical, Major, Minor) can use the subtle accent colors (muted red/green) for quick identification, but the primary display should remain text-based.
*   **Document Analyzer/Research Assistant**: When context is retrieved, it should be clearly indicated, perhaps with a subtle `[Context from Document]` tag or a distinct, slightly indented text block.

### 5.3. Input Bar

*   **Location**: Fixed at the bottom of the main content area.
*   **Design**: A sleek, subtle text input field. It should be a simple rectangle with a 1px border, blending seamlessly with the overall dark theme. A placeholder text like `> Type a command or query...` should be present.
*   **Send Button**: A minimalist send button (e.g., a simple arrow icon) to the right of the input field.

## 6. Interactivity and Responsiveness

*   **Subtle Animations**: Avoid flashy animations. Use subtle transitions for state changes (e.g., persona switching, message loading) to enhance the premium feel without distracting the user.
*   **Responsiveness**: The layout must be fully responsive, adapting gracefully to different screen sizes (desktop, tablet, mobile) while maintaining the core aesthetic.

## 7. Adaptation to Project Features

*   **Persona Integration**: The frontend must dynamically load persona metadata from `/api/personas` and adjust its behavior (e.g., showing/hiding upload zones, rendering structured vs. freeform output) based on the `output_mode` and `requires_upload` flags from the backend.
*   **History Management**: Each persona should maintain its own chat history, displayed in the main content area when selected.
*   **File Uploads**: The upload mechanism should be integrated cleanly, perhaps appearing as a subtle attachment icon near the input bar, with uploaded file details displayed minimally.

## 8. Visual Reference

Refer to the attached image `elite_terminal_code_review.png` for the overall aesthetic and feel. Note that the implementation should *adapt* this visual to the project's specific features and the requested left-side menu bar, rather than replicating it pixel-for-pixel. The image serves as a guide for the desired professional, sleek, and structured terminal-inspired look.
