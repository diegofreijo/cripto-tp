#include <list.h>

typedef enum { UNA_CARTA, AL_MAZO, UN_CANTO } jugadasPosibles;
typedef enum { ORO, COPA, ESPADA, BASTO } palo;


class carta
{
  public:
    carta( palo PelPalo, int PelNumero )
    {
      this->elPalo = PelPalo;
      this->elNumero = PelNumero;
    }
    carta( void )
    {
      this->elPalo = ORO;
      this->elNumero = -1;
    }
    char elPaloAsChar( void )
    {
      switch(this->elPalo)
      {
        case ORO: return 'O';
        case COPA: return 'C';
        case ESPADA: return 'E';
        case BASTO: return 'B';
      }
      return '?';
    }
    int valorRelativo( void )
    {
      if( elNumero == 4 ) return 0;
      if( elNumero == 5 ) return 1;
      if( elNumero == 6 ) return 2;
      if( elNumero == 7 && (elPalo == COPA || elPalo == BASTO) ) return 3;
      if( elNumero == 10 ) return 4;
      if( elNumero == 11 ) return 5;
      if( elNumero == 12 ) return 6;
      if( elNumero == 1 && (elPalo == COPA || elPalo == ORO) ) return 7;
      if( elNumero == 2 ) return 8;
      if( elNumero == 3 ) return 9;
      if( elNumero == 7 && elPalo == ORO ) return 10;
      if( elNumero == 7 && elPalo == ESPADA ) return 11;
      if( elNumero == 1 && elPalo == BASTO ) return 12;
      if( elNumero == 1 && elPalo == ESPADA ) return 13;
      return -1;
    }
    static bool mata( carta carta1, carta carta2 )
    {
      return carta1.valorRelativo() > carta2.valorRelativo();
    }
    bool operator ==( carta carta2 )
    {
      return this->elPalo == carta2.elPalo && this->elNumero == carta2.elNumero;
    }
    palo elPalo;
    int elNumero;
};


class jugada
{
  public:
    jugada( jugadasPosibles PtipoDeJugada, carta PLaCarta )
    {
      this->tipoDeJugada = PtipoDeJugada;
      this->LaCarta = PLaCarta;
    }
    jugadasPosibles tipoDeJugada;
    carta LaCarta;
};


class ManoTruco
{
  public:
    ManoTruco( list<carta> cartasIniciales, bool soyMano )
    {
      this->_soyMano = soyMano;
      this->_cartasQueTengo = cartasIniciales;

      // inicializacion del estado
      this->_esMiTurno = soyMano;
      this->_fuiManoEnSubManoActual = soyMano;
      this->_subManoActual = 1;
      this->_vieneParda = false;
    }
    bool soyMano( void )
    {
      // """True si soy mano (no soy pie, reparti yo, y fui mano en la primera submano), False si no."""
      return this->_soyMano;
    }

    bool subManoActual( void )
    {
      // """Mano actual, de 1 a 3. 0 si el juego esta terminado"""
      return this->_subManoActual;
    }

    bool terminado( void )
    {
      return this->_subManoActual == 0;
    }

    bool turnoDeJuego( void ) // true si me toca a mi. False si ya terminamos o si le toca al otro
    {
      // """A quién le toca jugar. Notar que NO ES LO MISMO que soyMano()"""
      if( terminado() ) return false;
      return this->_esMiTurno;
    }

    void jugadasPosibles( list<jugada> *JugadasPosibles )
    {
      /*
      # esto seria: for each _cartasQueTengo armar una jugada que sea poner esa carta y agregarla a una lista, y retornar esa lista
      # Si _esMiTurno (llamo a turnoDeJuego) muestro las siguientes opciones
      # Para el caso de las cartas en juego muestro la lista _cartasQueTengo
      # Para el caso de Envido
      #   Si no jugue ninguna carta, y estadoEnvido.valor()>=0 o estadoEnvido.valor()<5
      #     muestro estadoEnvido.codigo() para estadoEnvido.valor() en [estadoEnvido.valor()+1,4]
      #   Si no jugue ninguna carta, y estadoEnvido.valor()>=5 y estadoEnvido.codigo='QUIERO' y _soyMano
      #     muestro las opciones de TENGO TANTO (calculo el envido que tengo)
      #   Si no jugue ninguna carta, y estadoEnvido.valor()>=5 y estadoEnvido.codigo='QUIERO' y not _soyMano
      #     muestro las opciones de TANTO SON MEJORES (calculo el envido que tengo)
      #     muestro las opciones de SON BUENAS
      # Para el caso de Truco
      #   Si estadoTruco.valor()>=0 o estadoTruco.valor()<4
      #     muestro estadoTruco.codigo()+ 1
      #   Si estadoTruco.valor()>=4
      #     no muestro nada porque esta todo cantado
      */

      // genero una jugada posible para cada carta que puedo jugar
      for( list<carta>::iterator list_iter = _cartasQueTengo.begin();
           list_iter != _cartasQueTengo.end(); list_iter++)
      {
        JugadasPosibles->push_back( jugada( UNA_CARTA, *list_iter ) );
      }
    }

    bool jugar( jugada laJugada )
    {
      if( !this->_esMiTurno ) return false;

      /*
      """realizar una lista de jugadas (o sea, Cantos y/o Cartas) que hace esta parte"""
      # si me voy al mazo, perdi, y es el fin del juego
      # extraigo carta de la jugada y la guardo como _juegoMio
      # sacar carta jugada de la lista _cartasQueTengo
      # si no _fuiManoEnSubManoActual, termina una submano
      */
      _juegoMio = laJugada.LaCarta;
      _cartasQueTengo.remove( _juegoMio ); // ojo que acá no estoy validando que la carta sea una de las mias!
      if( !this->_fuiManoEnSubManoActual )
      {
        _terminaSubMano();
      }
      else
      {
        // # si _fuiManoEnSubManoActual, le cambia el turno (le toca al otro) y nada mas
        this->_esMiTurno = !this->_esMiTurno;
      }
      /*
      # me parece que esta funcion la tiene que invocar el usuario cuando selecciona una opcion. Por lo tanto, lo que hay que hacer es procesarla y ver los cambios que pueden producir
      # como se que tipo de jugada es?? Aca es donde decian que hacia falta la clase Jugada??
      # Si se juega una carta
      #   la agrego a la lista _juegoOtro y si len(_juegoOtro)==len(_juegoMio)==_subManoActual
      #       me fijo cual de los dos gano la mano. Si soy yo entonces _esMiTurno=1 (aca tendria que llamar a turnoDeJuego)
      # Si juego un canto de Envido
      #   debo actualizar los puntos en juego del envido querido y no querido
      #   si jugada=ENVIDO, _PtosEnvidoQuerido=2,_PtosEnvidoNQuerido=1
      #   si jugada=ENVIDOENVIDO, _PtosEnvidoQuerido+=2,_PtosEnvidoNQuerido+=1
      #   si jugada=REALENVIDO, _PtosEnvidoQuerido+=3,_PtosEnvidoNQuerido+=1
      #   si jugada=FALTAENVIDO, _PtosEnvidoQuerido+=2,_PtosEnvidoNQuerido+=1 (puede ser que termine el juego. Hay que ver el Score)
      #   si jugada=QUIERO, no incremento el score.Luego en el menu va a aprecer la opcion TENGO TANTO
      #   si jugada=NOQUIERO, no incremento el score
      # Si juego un canto de Truco
      #   si jugada=TRUCO, _PtosTrucoQuerido+=2,_PtosTrucoNQuerido+=1
      #   si jugada=RETRUCO, _PtosEnvidoQuerido+=1,_PtosEnvidoNQuerido+=1
      #   si jugada=VALE4, _PtosEnvidoQuerido+=1,_PtosEnvidoNQuerido+=1
      #   si jugada=QUIERO, no incremento el score. Cuando se termine la mano veo quien gano y actualizo el score
      #   si jugada=NOQUIERO, no incremento el score. Cuando se termine la mano veo quien gano y actualizo el score
      # Si se jugaba un canto de carta y canto se dividia en dos y se trataba por separado sin necesidad de preguntar dos veces??
      */
      return true;
    }

    bool recibirJugada( jugada laJugada )
    {
      if( this->_esMiTurno ) return false;

      _juegoOtro = laJugada.LaCarta;
      if( this->_fuiManoEnSubManoActual )
      {
        _terminaSubMano();
      }
      else
      {
        // # si !_fuiManoEnSubManoActual, le cambia el turno (le toca al otro) y nada mas
        this->_esMiTurno = !this->_esMiTurno;
      }
      return true;
    }

    bool ganeYo( void )
    {
      if( !terminado() ) return false;
      return _ganeYo;
    }

  private:
    bool _soyMano; // esta en 1 si es el servidor, si no, 0
    bool _ganeYo;
    list<carta> _cartasQueTengo; // una lista que contiene las posibles cartas a jugar. Cuando se juega una, se la saca de la lista
    int _subManoActual; // numero de mano que se esta jugando 1,2,3
    bool _esMiTurno; // vale 1 si soy mano en _manoEnSubManoActual o si me llega un canto del otro lado y tengo que responder
    bool _vieneParda; // vale 1 si el que mata gana
    bool _ganePrimera;
    bool _fuiManoEnSubManoActual;
    carta _juegoMio; // =None     # me parece mejoruno  que _cartaMiaEnSubManoActual = None
    carta _juegoOtro; // =None  # me parece mejor que _cartaContricanteEnSubManoActual = None

    void _terminaSubMano( void )
    {
      /*
      #   el que mata, sigue jugando
      #   si parda la primera, sigue la mano
      #   si parda la segunda, gana la primera. Si parda la primera sigue la mano
      #   si juego la tercera, y no _fuiManoEnSubManoActual, entonces es el fin del juego
      */
      if( carta::mata( _juegoMio, _juegoOtro ) )
      {
        if( _subManoActual == 1 ) _ganePrimera = true;
        if( _vieneParda || _subManoActual == 3 ||
            ( _subManoActual == 2 && _ganePrimera ) )
        {
          // gane
          _subManoActual = 0;
          _ganeYo = true;
          return;
        }
        _esMiTurno = true;
      }
      else
      {
        if( carta::mata( _juegoOtro, _juegoMio ) )
        {
          if( _subManoActual == 1 ) _ganePrimera = false;
          if( _vieneParda || _subManoActual == 3 ||
              ( _subManoActual == 2 && !_ganePrimera ) )
          {
            // perdi
            _subManoActual = 0;
            _ganeYo = false;
            return;
          }
          _esMiTurno = false;
        }
        else
        {
          _esMiTurno = _soyMano; // parda! sigue la mano
          if( _subManoActual == 3 )
          {
            // todo parda! gana la mano!
            _subManoActual = 0;
            _ganeYo = _soyMano;
            return;
          }
          if( _subManoActual == 2 )
          {
            // si parda la segunda, gana el que hizo primera
            // salvo que la primera haya sido parda tambien...
            if( !_vieneParda )
            {
              // gana el que hizo primera
              _subManoActual = 0;
              _ganeYo = _ganePrimera;
              return;
            }
          }
          _vieneParda = true;
        }
      }

      _subManoActual++;
      _fuiManoEnSubManoActual = _esMiTurno;
    }
};
