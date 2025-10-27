## Main Steps
1. Implement Vercel deployment
2. Implement translation functionality by calling OpenAI
3. Connect to the external database Supabase

## Challenges Encountered and Solutions
1. Sometimes AI cannot identify correct code errors, and continuous modifications may lead to more errors or new issues. It is necessary to commit code changes in a timely manner to enable reverting to previous versions.

2. When AI writes code, it often installs incorrect versions of environments, leading to program errors.

## Lessons Learned
1. Setting up the environment is crucial; otherwise, the program cannot run properly.Meanwhile, you need to run the program multiple times, check the version of the installed environment, and make continuous adjustments until the program runs normally.

2. External credentials (API tokens) must be managed carefully and stored in .env.

3. Attention should be paid to the public accessibility of GitHub repositories during deployment.

4. If a program has unexpectedly accumulated many errors, do not let AI modify it anymore; it is more time-efficient to start over.