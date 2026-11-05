# Project Reflection – Hostel Maintenance Ticket Sorter

## Introduction

The Hostel Maintenance Ticket Sorter is a Python-based project designed to improve the process of handling student maintenance complaints. The main objective is to classify complaints, identify urgent issues, assign appropriate maintenance teams, detect duplicate complaints, and organize maintenance tickets efficiently.

## Learning Experience

Through this project, I learned how artificial intelligence and Python programming can work together to solve real-world problems. I understood how an LLM can extract useful information from natural-language complaints and return structured JSON output.

I also improved my knowledge of Python concepts such as functions, dictionaries, lists, file handling, CSV operations, exception handling, regular expressions, and date calculations. Working with these concepts helped me understand how individual programming components can be combined into a complete application.

## Challenges Faced

One major challenge was designing a reliable prompt that produces consistent JSON responses. Another challenge was validating room numbers and identifying urgent complaints correctly.

Duplicate detection was also important because multiple students may report the same maintenance problem. I implemented duplicate identification using room number and issue category. This allows repeated complaints to be linked to an existing ticket instead of creating unnecessary tickets.

I also faced challenges during testing and debugging. Running red-team tests helped me understand how unusual inputs, invalid room numbers, and repeated complaints should be handled.

The current implementation uses a local mock classifier. Live Gemini API integration remains a future development task.

## Importance of Human Supervision

I learned that AI should not make every decision independently, especially when safety is involved. The system identifies urgent complaints and organizes maintenance tickets, but the warden remains responsible for reviewing urgent cases, assigning maintenance work, and deciding when tickets can be closed.

This approach improves accountability and supports responsible AI development.

## Future Improvements

In the future, the project can be improved by completing live LLM integration through an approved API connection, developing a graphical user interface, adding student login facilities, and providing real-time ticket status updates.

Additional testing with different complaint formats can also improve classification reliability.

## Conclusion

Overall, this project helped me understand how AI can be combined with traditional programming to develop practical solutions. It improved my technical knowledge, problem-solving ability, debugging skills, and understanding of responsible AI development. I also learned that testing, validation, documentation, and human supervision are essential for building reliable AI applications.