/**
 * Menu openen/sluiten op kleine schermen en submenu's toegankelijk maken.
 * Gebaseerd op navigation.js uit het Twenty Twelve-thema, zonder jQuery.
 */
( function() {
	var nav = document.getElementById( 'site-navigation' ), button, menu;
	if ( ! nav ) {
		return;
	}

	button = nav.getElementsByTagName( 'button' )[0];
	menu   = nav.getElementsByTagName( 'ul' )[0];
	if ( ! button || ! menu ) {
		return;
	}

	button.onclick = function() {
		var open = button.classList.toggle( 'toggled-on' );
		menu.classList.toggle( 'toggled-on', open );
		button.setAttribute( 'aria-expanded', open ? 'true' : 'false' );
	};

	// Submenu tonen bij toetsenbordfocus.
	nav.querySelectorAll( 'a' ).forEach( function( link ) {
		function setFocus( on ) {
			var el = link.parentElement;
			while ( el && el !== nav ) {
				if ( el.classList.contains( 'page_item' ) ) {
					el.classList.toggle( 'focus', on );
				}
				el = el.parentElement;
			}
		}
		link.addEventListener( 'focus', function() { setFocus( true ); } );
		link.addEventListener( 'blur', function() { setFocus( false ); } );
	} );

	// Op aanraakschermen opent de eerste tik het submenu.
	if ( 'ontouchstart' in window ) {
		nav.querySelectorAll( '.page_item_has_children > a' ).forEach( function( link ) {
			link.addEventListener( 'touchstart', function( e ) {
				var li = link.parentElement;
				if ( ! li.classList.contains( 'focus' ) ) {
					e.preventDefault();
					nav.querySelectorAll( '.page_item.focus' ).forEach( function( other ) {
						other.classList.remove( 'focus' );
					} );
					li.classList.add( 'focus' );
				}
			} );
		} );
	}
} )();
