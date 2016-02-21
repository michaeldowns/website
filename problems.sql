INSERT INTO problems (title, text, difficulty, solution)
VALUES (
'Mean and Standard Deviation',
'The <a href="/static/problem_data/problem_1.txt">data</a> for this problem was generated from a normal distribution with mean $\mu$ and variance $\sigma^2$. Rounding calculations to integers where necessary, determine $\frac{\mu}{\sigma}$',
1,
'57'
);

INSERT INTO problems (title, text, difficulty, solution)
VALUES (
'Basis Function Regression',
'The <a href="/static/problem_data/problem_2.txt">data</a> for this problem is of the form $(x_i, y_i)$ where $y_i = \sum_{j=1}^{n} \theta_j\phi_j(x_i) + \epsilon_i$, $\theta_j$ are constants, $\phi_j$ are functions of $x_i$, and $\epsilon_i \sim \mathcal{N}(0, 1)$. You are given that each $\phi_j$ is either a monomial or a trigonometric function. Using least squares to recover the regression coefficients, determine $\sum_{j=1}^{n} \theta_j$.',
2,
'313'
);
