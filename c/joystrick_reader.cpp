#include <stdio.h>
#include "SDL.h"
#include <unistd.h>


signed short position_x ()
{
	if ( SDL_InitSubSystem ( SDL_INIT_JOYSTICK ) < 0 )
	{
		fprintf ( stderr, "Unable to initialize Joystick: %s\n", SDL_GetError() );
		return -1;
	}

	//printf ( "%i joysticks found\n", SDL_NumJoysticks () );
	
	SDL_Joystick* joy1 = SDL_JoystickOpen ( 0 );

	if ( joy1 == NULL )
		printf ( "could not open joystick\n" );

	/*printf ( "%i achsen\n", SDL_JoystickNumAxes ( joy1 ) );
	printf ( "%i rollbaelle\n", SDL_JoystickNumBalls ( joy1 ) );
	printf ( "%i heads\n", SDL_JoystickNumHats ( joy1 ) );
	printf ( "%i koepfe\n", SDL_JoystickNumButtons ( joy1 ) );*/

	//SDL_JoystickEventState (SDL_ENABLE);
	// this will alter the behaviour of the event queue of the sdl system
	SDL_JoystickEventState ( SDL_QUERY );

	//while ( 1 )
	//{
		SDL_JoystickUpdate ();

		signed short a = SDL_JoystickGetAxis ( joy1, 1 );
                a = SDL_JoystickGetAxis ( joy1, 1 );
                if(a>=28000) a=28000;
                if(a<=-28000) a=-28000;
                a = (a + 28000) * 50 / 56000;
		//printf ( "axis %i is %d\n", 1,a );
                /*signed short b = SDL_JoystickGetAxis ( joy1, 0 );
                b = SDL_JoystickGetAxis ( joy1, 0 );
                if(b>=28000) b=28000;
                if(b<=-28000) b=-28000;
                b = 0 - b * 90 / 28000;*/ 
                //printf ( "axis %i is %d\n", 0,b );
                //sleep(1);
	//}
	return a;
}
signed short position_y ()
{
        if ( SDL_InitSubSystem ( SDL_INIT_JOYSTICK ) < 0 )
        {
                fprintf ( stderr, "Unable to initialize Joystick: %s\n", SDL_GetError() );
                return -1;
        }

        //printf ( "%i joysticks found\n", SDL_NumJoysticks () );
        
        SDL_Joystick* joy1 = SDL_JoystickOpen ( 0 );

        if ( joy1 == NULL )
                printf ( "could not open joystick\n" );

        /*printf ( "%i achsen\n", SDL_JoystickNumAxes ( joy1 ) );
        printf ( "%i rollbaelle\n", SDL_JoystickNumBalls ( joy1 ) );
        printf ( "%i heads\n", SDL_JoystickNumHats ( joy1 ) );
        printf ( "%i koepfe\n", SDL_JoystickNumButtons ( joy1 ) );*/

        //SDL_JoystickEventState (SDL_ENABLE);
        // this will alter the behaviour of the event queue of the sdl system
        SDL_JoystickEventState ( SDL_QUERY );

        //while ( 1 )
        //{
                SDL_JoystickUpdate ();

                /*signed short a = SDL_JoystickGetAxis ( joy1, 1 );
                a = SDL_JoystickGetAxis ( joy1, 1 );
                if(a>=28000) a=28000;
                if(a<=-28000) a=-28000;
                a = (a + 28000) * 50 / 56000;*/
                //printf ( "axis %i is %d\n", 1,a );
                signed short b = SDL_JoystickGetAxis ( joy1, 0 );
                b = SDL_JoystickGetAxis ( joy1, 0 );
                if(b>=28000) b=28000;
                if(b<=-28000) b=-28000;
                b = 0 - b * 90 / 28000;
                //printf ( "axis %i is %d\n", 0,b );
                //sleep(1);
        //}
        return b;
}
