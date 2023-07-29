import time
from decimal import Decimal

# Exemplo usando números de ponto flutuante (float)


if __name__ == "__main__":
    start_time_float = time.time()
    x_float = 1.0
    y_float = 3.0
    resultado_float = x_float / y_float
    end_time_float = time.time()
    print("Tempo com float:", end_time_float - start_time_float)

    # Exemplo usando a biblioteca decimal
    # getcontext().prec = 50  # Definindo a precisão para 50 casas decimais
    start_time_decimal = time.time()
    x_decimal = Decimal("1.0")
    y_decimal = Decimal("3.0")
    resultado_decimal = x_decimal / y_decimal
    end_time_decimal = time.time()
    print("Tempo com decimal:", end_time_decimal - start_time_decimal)
