## Lab 2 writeup

---

## Main Steps
1. Implement Vercel deployment
2. Implement translation functionality by calling OpenAI

---

## Challenges Encountered and Solutions

1. Sometimes AI cannot identify correct code errors, and continuous modifications may lead to more errors or new issues.
It is necessary to commit code changes in a timely manner to enable reverting to previous versions.

2. Deployment recognition error (Vercel identifies src as a Node project):
Cause: Vercel guesses the builder based on the directory structure in simple projects. The repository does not have a top-level package.json, but there are front-end static files in src, leading to Vercel's incorrect guess.
Solution: Add vercel.json to explicitly specify that src/main.py uses @vercel/python, and handle the static folder as a static builder with clear routing.

3. Security and credential management for the translation API:
The project's src/models/llm.py reads the environment variable GITHUB_TOKEN (your .env already contains this token). Putting the token in .env facilitates local development, but real tokens should not be committed to public repositories.

  


## Lessons Learned

1. Setting up the environment is crucial; otherwise, the program cannot run properly.

2. External credentials (API tokens) must be managed carefully and stored in .env.

3. Attention should be paid to the public accessibility of GitHub repositories during deployment.



---



。

---


