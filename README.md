# UECE-Programacao_Concorrente
Descrição do Problema do Aeroporto de Pista Única

Trata-se de projetar e implementar um programa concorrente para automatizar um controle de tráfego aéreo sem torre de controle. Nesse aeroporto contém uma única pista, na qual todas as aeronaves devem utilizar tanto para decolarem como aterrissarem. Portanto, a pista só pode ser utilizada exclusivamente por um único avião por vez.

Há uma fila tanto para decolagem como para aterrisagem. O tamanho máximo é de três aeronaves em cada fila.

O total de aeronaves que serão gerenciadas é de dezoito, sendo nove delas que desejam aterrissar e as outras noves que desejam decolar. A ordem é aleatória dessas aeronaves.

Algumas considerações e restrições sobre o problema apresentado:
- As aeronaves que desejam decolar devem esperar cinco segundos antes de iniciar a ação de decolar em relação a aeronave anterior que tenha aterrissado ou da aeronave que tenha acabado de decolado.
- As aeronaves que desejam decolar precisam de mais cinco segundos de posse da pista para realizar essa ação.
- As aeronaves que desejam aterrissar precisam de dez segundos de posse da pista para completar a sua ação com segurança.
- A prioridade para uso da pista sempre será para as aeronaves que desejam aterrissar. Contudo, caso a fila de decolagem esteja cheia e que haja tempo de combustível suficiente para as aeronaves que desejam aterrissar ficarem no ar, a prioridade será alterada para as aeronaves que desejam decolar.
- A aeronave que tenha sido gerado com a ação de aterrissar terá acesso imediato a pista, caso essa esteja liberada, se não, terá acesso no exato momento que a pista for liberada.
- O tempo máximo que cada aeronave por ficar no ar é de trinta segundos.
- O tempo de diferença para geração de cada aeronave é de sete segundos e a sua ação entre decolar ou aterrissar é escolhida de forma aleatória, como já foi mencionado. 
- Não pode ocorrer colisão na pista na decolagem e nem deixar nenhuma aeronave caia por falta de combustível, ou seja, que fique mais do que trinta segundos no ar. 

Obs.: O código por conter alguns bugs, por favor reportar. 
Obrigado.
