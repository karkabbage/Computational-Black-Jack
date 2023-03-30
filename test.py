import BlackJack_Game as bj

def test() -> None:
    wins = []
    for _ in range(0, 10000):
        black_jack = bj.BlackJack()
        result = black_jack.run_game()
        assert result != 'U fucked up and forgot a case'
        wins.append(result)

    print(len([win for win in wins if win == 'Player Wins']) / len(wins))


if __name__ == '__main__':
    import pytest
    pytest.main(['test.py'])
