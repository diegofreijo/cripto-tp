#include "manotruco.cpp"

void mostrarOpcionesyJugar( ManoTruco *truc, ManoTruco *aQuienAviso )
{
  list<jugada> jugadas;
  int opcion = 1;
  truc->jugadasPosibles( &jugadas );

  for( list<jugada>::iterator list_iter = jugadas.begin();
       list_iter != jugadas.end(); list_iter++)
  {
    if( list_iter->tipoDeJugada == UNA_CARTA )
    {
      cout << "Opcion " << opcion << ": jugar el ";
      cout << list_iter->LaCarta.elNumero << " de " << list_iter->LaCarta.elPaloAsChar() << endl;
      opcion++;
    }
  }
  cin >> opcion;

  for( list<jugada>::iterator list_iter = jugadas.begin();
       list_iter != jugadas.end(); list_iter++)
  {
    opcion--;
    if( opcion == 0 )
    {
      truc->jugar( *list_iter );
      aQuienAviso->recibirJugada( *list_iter );
      break;
    }
  }
}

int main( void )
{
  list<carta> cartas1;
  cartas1.clear();
  cartas1.push_back( carta( ORO, 1 ) );
  cartas1.push_back( carta( ORO, 2 ) );
  cartas1.push_back( carta( ORO, 3 ) );

  list<carta> cartas2;
  cartas2.clear();
  cartas2.push_back( carta( ESPADA, 1 ) );
  cartas2.push_back( carta( ESPADA, 2 ) );
  cartas2.push_back( carta( ESPADA, 3 ) );

  list<jugada> jugadas;
  ManoTruco truc1( cartas1, true );
  ManoTruco truc2( cartas2, false );

  while( !truc1.terminado() || !truc2.terminado() )
  {
    if( truc1.turnoDeJuego() )
    {
      mostrarOpcionesyJugar( &truc1, &truc2 );
    }
    if( truc2.turnoDeJuego() )
    {
      jugadas.clear();
      truc2.jugadasPosibles( &jugadas );
      truc2.jugar( *( jugadas.begin() ) );
      /* avisar al otro jugador lo que jugo la compu */
      truc1.recibirJugada( *( jugadas.begin() ) );
      cout << "La compu juega el " << jugadas.begin()->LaCarta.elNumero;
      cout << " de " <<  jugadas.begin()->LaCarta.elPaloAsChar() << endl;
    }
  }
  if( truc1.ganeYo() )
  {
    cout << "bien! ganaste!" << endl;
  }
  else
  {
    cout << "looser!" << endl;
  }
  system("pause");
  return 0;
}
