/* Reinmarc — interactie */
( function() {
	'use strict';

	var reduceMotion = window.matchMedia( '(prefers-reduced-motion: reduce)' ).matches;

	/* ---------- Kop: schaduw bij scrollen + mobiel menu ---------- */

	var header = document.querySelector( '.site-header' );
	if ( header ) {
		var onScroll = function() {
			header.classList.toggle( 'is-scrolled', window.scrollY > 8 );
		};
		window.addEventListener( 'scroll', onScroll, { passive: true } );
		onScroll();
	}

	var toggle = document.querySelector( '.nav-toggle' );
	var nav = document.getElementById( 'main-nav' );
	if ( toggle && nav ) {
		var setOpen = function( open ) {
			toggle.setAttribute( 'aria-expanded', open ? 'true' : 'false' );
			toggle.setAttribute( 'aria-label', open ? 'Menu sluiten' : 'Menu openen' );
			nav.classList.toggle( 'is-open', open );
		};
		toggle.addEventListener( 'click', function() {
			setOpen( toggle.getAttribute( 'aria-expanded' ) !== 'true' );
		} );
		document.addEventListener( 'keydown', function( e ) {
			if ( e.key === 'Escape' && nav.classList.contains( 'is-open' ) ) {
				setOpen( false );
				toggle.focus();
			}
		} );
		document.addEventListener( 'click', function( e ) {
			if ( nav.classList.contains( 'is-open' ) && ! nav.contains( e.target ) && ! toggle.contains( e.target ) ) {
				setOpen( false );
			}
		} );
	}

	/* ---------- Verschijnen bij scrollen ---------- */

	var revealEls = document.querySelectorAll( '[data-reveal]' );
	if ( 'IntersectionObserver' in window && ! reduceMotion ) {
		var io = new IntersectionObserver( function( entries ) {
			entries.forEach( function( entry ) {
				if ( entry.isIntersecting ) {
					entry.target.classList.add( 'is-visible' );
					entry.target.dispatchEvent( new CustomEvent( 'revealed' ) );
					io.unobserve( entry.target );
				}
			} );
		}, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 } );
		revealEls.forEach( function( el ) {
			io.observe( el );
		} );
	} else {
		revealEls.forEach( function( el ) {
			el.classList.add( 'is-visible' );
		} );
	}

	/* ---------- Vaste willekeur (zelfde patroon bij elke keer laden) ---------- */

	function seeded( seed ) {
		return function() {
			seed = ( seed * 16807 ) % 2147483647;
			return ( seed - 1 ) / 2147483646;
		};
	}

	/* ---------- Raam met ramenwisser ---------- */

	var win = document.querySelector( '[data-window]' );
	if ( win ) {
		initWindow( win );
	}

	function initWindow( root ) {
		var pane = root.querySelector( '.window-pane' );
		var canvas = pane.querySelector( 'canvas' );
		var sq = root.querySelector( '.squeegee' );
		var hint = root.parentNode.querySelector( '.window-hint' );
		var hintText = hint ? hint.querySelector( 'span' ) : null;
		var btnClean = root.parentNode.querySelector( '[data-clean]' );
		var btnSoap = root.parentNode.querySelector( '[data-soap]' );
		var ctx = canvas.getContext( '2d' );
		var W = 0, H = 0, dpr = 1;
		var rows = 3;
		var state = 'dirty';
		var running = false;
		var idleTimer = null;
		var dragging = false;
		var pointerId = null;
		var last = null;
		var needsResize = false;
		var afterRun = null;

		function blade() {
			return ( H / rows ) * 1.18;
		}

		function size() {
			var r = pane.getBoundingClientRect();
			dpr = Math.min( window.devicePixelRatio || 1, 2 );
			W = r.width;
			H = r.height;
			canvas.width = Math.round( W * dpr );
			canvas.height = Math.round( H * dpr );
			ctx.setTransform( dpr, 0, 0, dpr, 0, 0 );
			var b = blade();
			sq.style.height = b + 'px';
			sq.style.width = ( b * 0.62 ) + 'px';
		}

		function soap() {
			var rnd = seeded( 7 );
			var i, x, y, r, g;
			ctx.globalCompositeOperation = 'source-over';
			ctx.clearRect( 0, 0, W, H );
			ctx.fillStyle = 'rgba(232, 242, 247, 0.9)';
			ctx.fillRect( 0, 0, W, H );

			// Sopvegen
			for ( i = 0; i < 16; i++ ) {
				ctx.beginPath();
				ctx.moveTo( rnd() * W, rnd() * H );
				ctx.bezierCurveTo( rnd() * W, rnd() * H, rnd() * W, rnd() * H, rnd() * W, rnd() * H );
				ctx.lineWidth = 8 + rnd() * 26;
				ctx.lineCap = 'round';
				ctx.strokeStyle = 'rgba(255, 255, 255, ' + ( 0.35 + rnd() * 0.4 ) + ')';
				ctx.stroke();
			}

			// Schuim
			for ( i = 0; i < 170; i++ ) {
				x = rnd() * W;
				y = rnd() * H;
				r = 3 + rnd() * ( W / 30 );
				g = ctx.createRadialGradient( x, y, 0, x, y, r );
				g.addColorStop( 0, 'rgba(255, 255, 255, 0.95)' );
				g.addColorStop( 1, 'rgba(255, 255, 255, 0)' );
				ctx.fillStyle = g;
				ctx.beginPath();
				ctx.arc( x, y, r, 0, Math.PI * 2 );
				ctx.fill();
			}

			// Belletjes
			ctx.lineWidth = 1.2;
			for ( i = 0; i < 60; i++ ) {
				ctx.beginPath();
				ctx.arc( rnd() * W, rnd() * H, 1.5 + rnd() * 5, 0, Math.PI * 2 );
				ctx.strokeStyle = 'rgba(140, 180, 200, 0.55)';
				ctx.stroke();
			}
			state = 'dirty';
		}

		function eraseLine( x0, y0, x1, y1, width, cap ) {
			ctx.globalCompositeOperation = 'destination-out';
			ctx.lineCap = cap;
			ctx.lineWidth = width;
			ctx.strokeStyle = '#000';
			ctx.beginPath();
			ctx.moveTo( x0, y0 );
			ctx.lineTo( x1, y1 );
			ctx.stroke();
		}

		function placeSqueegee( x, y, dir ) {
			var b = blade();
			var w = b * 0.62;
			// Het rubber zit rechts in de tekening (op 78% van de breedte)
			var bladeX = w * 0.78;
			sq.style.transform = 'translate(' + ( x - bladeX ) + 'px,' + ( y - b / 2 ) + 'px)' + ( dir < 0 ? ' scaleX(-1)' : '' );
			sq.style.transformOrigin = bladeX + 'px 50%';
		}

		function ease( t ) {
			return t < 0.5 ? 2 * t * t : 1 - Math.pow( -2 * t + 2, 2 ) / 2;
		}

		// Veeg rij voor rij, zoals een glazenwasser: heen en terug.
		function autoWipe( fromRow, toRow, done ) {
			if ( running ) {
				return;
			}
			running = true;
			sq.classList.add( 'is-active' );
			var row = fromRow;
			var b = blade();

			function doRow() {
				if ( row > toRow ) {
					sq.classList.remove( 'is-active' );
					running = false;
					if ( needsResize ) {
						needsResize = false;
						applyResize();
					}
					var next = afterRun;
					afterRun = null;
					if ( next ) {
						next();
					} else if ( done ) {
						done();
					}
					return;
				}
				var dir = row % 2 === 0 ? 1 : -1;
				var y = H * ( row + 0.5 ) / rows;
				var xStart = dir > 0 ? -b * 0.4 : W + b * 0.4;
				var xEnd = dir > 0 ? W + b * 0.4 : -b * 0.4;
				var prevX = xStart;
				var dur = 1100;
				var t0 = null;

				function frame( ts ) {
					if ( t0 === null ) {
						t0 = ts;
					}
					var t = Math.min( 1, ( ts - t0 ) / dur );
					var x = xStart + ( xEnd - xStart ) * ease( t );
					// Licht golvende lijn
					var yy = y + Math.sin( t * Math.PI * 2 ) * b * 0.06;
					eraseLine( prevX, yy, x, yy, b, 'butt' );
					placeSqueegee( x, yy, dir );
					prevX = x;
					if ( t < 1 ) {
						requestAnimationFrame( frame );
					} else {
						row++;
						setTimeout( doRow, 180 );
					}
				}
				requestAnimationFrame( frame );
			}
			doRow();
		}

		function clearedRatio() {
			var step = 12;
			var data = ctx.getImageData( 0, 0, canvas.width, canvas.height ).data;
			var total = 0, clear = 0;
			for ( var y = 0; y < canvas.height; y += step ) {
				for ( var x = 0; x < canvas.width; x += step ) {
					total++;
					if ( data[ ( y * canvas.width + x ) * 4 + 3 ] < 40 ) {
						clear++;
					}
				}
			}
			return clear / total;
		}

		function setHint( text, visible ) {
			if ( ! hint ) {
				return;
			}
			if ( text && hintText ) {
				hintText.textContent = text;
			}
			hint.classList.toggle( 'is-visible', visible );
			hint.classList.toggle( 'is-done', state === 'clean' );
		}

		function finish() {
			ctx.globalCompositeOperation = 'source-over';
			ctx.clearRect( 0, 0, W, H );
			state = 'clean';
			clearTimeout( idleTimer );
			sq.classList.remove( 'is-active' );
			setHint( 'Brandschoon.', true );
			btnClean.hidden = true;
			btnSoap.hidden = false;
		}

		function startDemo() {
			soap();
			btnClean.hidden = false;
			btnSoap.hidden = true;
			setHint( '', false );
			if ( reduceMotion ) {
				setHint( 'Veeg het raam zelf schoon', true );
				return;
			}
			setTimeout( function() {
				autoWipe( 0, 0, function() {
					setHint( 'Veeg de rest zelf schoon', true );
					scheduleIdle();
				} );
			}, 700 );
		}

		// Doet de bezoeker niets, dan maakt de ramenwisser het zelf af.
		function scheduleIdle() {
			clearTimeout( idleTimer );
			idleTimer = setTimeout( function() {
				if ( state === 'dirty' && ! dragging ) {
					setHint( '', false );
					autoWipe( 1, rows - 1, finish );
				}
			}, 7000 );
		}

		function point( e ) {
			var r = canvas.getBoundingClientRect();
			return { x: e.clientX - r.left, y: e.clientY - r.top };
		}

		canvas.addEventListener( 'pointerdown', function( e ) {
			if ( state !== 'dirty' || running || dragging ) {
				return;
			}
			dragging = true;
			pointerId = e.pointerId;
			canvas.setPointerCapture( e.pointerId );
			last = point( e );
			sq.classList.add( 'is-active' );
			placeSqueegee( last.x, last.y, 1 );
			clearTimeout( idleTimer );
			setHint( '', false );
		} );

		canvas.addEventListener( 'pointermove', function( e ) {
			if ( ! dragging || e.pointerId !== pointerId ) {
				return;
			}
			var p = point( e );
			eraseLine( last.x, last.y, p.x, p.y, blade() * 0.7, 'round' );
			placeSqueegee( p.x, p.y, p.x >= last.x ? 1 : -1 );
			last = p;
		} );

		function endDrag( e ) {
			if ( ! dragging || e.pointerId !== pointerId ) {
				return;
			}
			dragging = false;
			pointerId = null;
			sq.classList.remove( 'is-active' );
			if ( clearedRatio() > 0.93 ) {
				finish();
			} else if ( ! reduceMotion ) {
				scheduleIdle();
			}
		}

		canvas.addEventListener( 'pointerup', endDrag );
		canvas.addEventListener( 'pointercancel', endDrag );

		btnClean.addEventListener( 'click', function() {
			clearTimeout( idleTimer );
			setHint( '', false );
			if ( reduceMotion ) {
				finish();
			} else if ( running ) {
				afterRun = function() {
					autoWipe( 0, rows - 1, finish );
				};
			} else {
				autoWipe( 0, rows - 1, finish );
			}
		} );

		btnSoap.addEventListener( 'click', startDemo );

		function applyResize() {
			var wasClean = state === 'clean';
			size();
			if ( wasClean ) {
				finish();
			} else {
				soap();
			}
		}

		var resizeTimer;
		window.addEventListener( 'resize', function() {
			clearTimeout( resizeTimer );
			resizeTimer = setTimeout( function() {
				if ( running ) {
					needsResize = true;
				} else {
					applyResize();
				}
			}, 200 );
		} );

		size();
		startDemo();
	}

	/* ---------- Zeepbellen om kapot te tikken ---------- */

	var bubbleBox = document.querySelector( '.bubbles' );
	if ( bubbleBox && ! reduceMotion ) {
		var rndB = Math.random;
		var makeBubble = function( initial ) {
			var b = document.createElement( 'span' );
			var s = 18 + rndB() * 44;
			var dur = 14 + rndB() * 12;
			b.className = 'bubble';
			b.style.width = s + 'px';
			b.style.height = s + 'px';
			b.style.left = ( rndB() * 96 ) + '%';
			b.style.animationDuration = dur + 's';
			b.style.animationDelay = ( initial ? -rndB() * dur : 0 ) + 's';
			b.addEventListener( 'pointerdown', function() {
				b.classList.add( 'is-popped' );
				setTimeout( function() {
					b.remove();
					setTimeout( function() {
						makeBubble( false );
					}, 1500 );
				}, 300 );
			} );
			b.addEventListener( 'animationiteration', function() {
				b.style.left = ( rndB() * 96 ) + '%';
			} );
			bubbleBox.appendChild( b );
		};
		for ( var i = 0; i < 9; i++ ) {
			makeBubble( true );
		}
	}

	/* ---------- Voor / na ---------- */

	document.querySelectorAll( '.ba' ).forEach( function( ba ) {
		var buttons = ba.querySelectorAll( '.ba-switch button' );
		var label = ba.querySelector( '.ba-label' );
		var touched = false;

		function show( after ) {
			ba.classList.toggle( 'show-after', after );
			buttons[0].setAttribute( 'aria-pressed', after ? 'false' : 'true' );
			buttons[1].setAttribute( 'aria-pressed', after ? 'true' : 'false' );
			label.textContent = after ? 'Na' : 'Voor';
		}

		buttons[0].addEventListener( 'click', function() {
			touched = true;
			show( false );
		} );
		buttons[1].addEventListener( 'click', function() {
			touched = true;
			show( true );
		} );
		ba.querySelector( '.ba-frame' ).addEventListener( 'click', function() {
			touched = true;
			show( ! ba.classList.contains( 'show-after' ) );
		} );

		// Laat één keer zien wat het verschil is.
		ba.addEventListener( 'revealed', function() {
			setTimeout( function() {
				if ( ! touched ) {
					show( true );
				}
			}, 1400 );
		} );
	} );

	/* ---------- Osmose-proefje ---------- */

	var demo = document.querySelector( '[data-demo]' );
	if ( demo ) {
		initDemo( demo );
	}

	function initDemo( root ) {
		var glass = root.querySelector( '.demo-glass' );
		var svg = glass.querySelector( 'svg' );
		var tabs = root.querySelectorAll( '.demo-tabs button' );
		var btn = root.querySelector( '[data-dry]' );
		var result = root.querySelector( '.demo-result' );
		var ns = 'http://www.w3.org/2000/svg';
		var rnd = seeded( 42 );
		var tap = true;

		for ( var i = 0; i < 34; i++ ) {
			var x = 20 + rnd() * 360;
			var y = 20 + rnd() * 210;
			var r = 4 + rnd() * 10;
			var spot = document.createElementNS( ns, 'circle' );
			spot.setAttribute( 'class', 'spot' );
			spot.setAttribute( 'cx', x );
			spot.setAttribute( 'cy', y );
			spot.setAttribute( 'r', r * 0.85 );
			svg.appendChild( spot );
			var drop = document.createElementNS( ns, 'ellipse' );
			drop.setAttribute( 'class', 'drop' );
			drop.setAttribute( 'cx', x );
			drop.setAttribute( 'cy', y );
			drop.setAttribute( 'rx', r );
			drop.setAttribute( 'ry', r * 1.12 );
			svg.appendChild( drop );
		}
		for ( var j = 0; j < 4; j++ ) {
			var path = document.createElementNS( ns, 'path' );
			var sx = 40 + rnd() * 320;
			path.setAttribute( 'class', 'streak' );
			path.setAttribute( 'd', 'M' + sx + ' 10 q ' + ( rnd() * 30 - 15 ) + ' 110 ' + ( rnd() * 20 - 10 ) + ' 230' );
			svg.insertBefore( path, svg.firstChild );
		}

		function reset() {
			glass.classList.remove( 'is-dry' );
			btn.textContent = 'Laat het raam drogen';
			result.textContent = tap ?
				'Nat raam, gewassen met gewoon leidingwater. Wat blijft er over als het opdroogt?' :
				'Nat raam, gewassen met osmosewater. Wat blijft er over als het opdroogt?';
		}

		tabs.forEach( function( t, idx ) {
			t.addEventListener( 'click', function() {
				tap = idx === 0;
				tabs[0].setAttribute( 'aria-pressed', tap ? 'true' : 'false' );
				tabs[1].setAttribute( 'aria-pressed', tap ? 'false' : 'true' );
				glass.classList.toggle( 'is-tap', tap );
				reset();
			} );
		} );

		btn.addEventListener( 'click', function() {
			if ( glass.classList.contains( 'is-dry' ) ) {
				reset();
				return;
			}
			glass.classList.add( 'is-dry' );
			btn.textContent = 'Opnieuw nat maken';
			result.textContent = tap ?
				'Bij de verdamping van gewoon leidingwater blijven de opgeloste zouten achter waardoor je strepen krijgt.' :
				'Omdat deze in osmosewater niet meer aanwezig zijn krijg je een streeploos resultaat.';
		} );

		glass.classList.add( 'is-tap' );
		reset();
	}

	/* ---------- Fotoviewer portfolio ---------- */

	var gallery = document.querySelector( '.gallery' );
	var lb = document.querySelector( '.lightbox' );
	if ( gallery && lb && typeof lb.showModal === 'function' ) {
		var links = Array.prototype.slice.call( gallery.querySelectorAll( 'a' ) );
		var img = lb.querySelector( 'img' );
		var cap = lb.querySelector( 'figcaption' );
		var current = 0;
		var opener = null;
		var startX = null;
		var swiped = false;

		var showPhoto = function( i ) {
			current = ( i + links.length ) % links.length;
			var a = links[ current ];
			img.src = a.getAttribute( 'href' );
			img.alt = a.querySelector( 'img' ).alt;
			cap.textContent = 'Foto ' + ( current + 1 ) + ' van ' + links.length;
			var next = new Image();
			next.src = links[ ( current + 1 ) % links.length ].getAttribute( 'href' );
		};

		links.forEach( function( a, i ) {
			a.addEventListener( 'click', function( e ) {
				e.preventDefault();
				opener = a;
				showPhoto( i );
				lb.showModal();
			} );
		} );

		lb.querySelector( '.lb-prev' ).addEventListener( 'click', function() {
			showPhoto( current - 1 );
		} );
		lb.querySelector( '.lb-next' ).addEventListener( 'click', function() {
			showPhoto( current + 1 );
		} );
		lb.querySelector( '.lb-close' ).addEventListener( 'click', function() {
			lb.close();
		} );
		lb.addEventListener( 'click', function( e ) {
			if ( swiped ) {
				swiped = false;
				return;
			}
			if ( e.target === lb ) {
				lb.close();
			}
		} );
		lb.addEventListener( 'close', function() {
			if ( opener ) {
				opener.focus( { preventScroll: true } );
			}
		} );
		lb.addEventListener( 'keydown', function( e ) {
			if ( e.key === 'ArrowLeft' ) {
				showPhoto( current - 1 );
			} else if ( e.key === 'ArrowRight' ) {
				showPhoto( current + 1 );
			}
		} );
		lb.addEventListener( 'pointerdown', function( e ) {
			startX = e.clientX;
		} );
		lb.addEventListener( 'pointercancel', function() {
			startX = null;
		} );
		lb.addEventListener( 'pointerup', function( e ) {
			if ( startX === null ) {
				return;
			}
			var dx = e.clientX - startX;
			startX = null;
			if ( Math.abs( dx ) > 50 ) {
				swiped = true;
				showPhoto( current + ( dx < 0 ? 1 : -1 ) );
			}
		} );
	}

	/* ---------- E-mailadres kopiëren ---------- */

	document.querySelectorAll( '[data-copy]' ).forEach( function( btn ) {
		btn.addEventListener( 'click', function() {
			var msg = btn.parentNode.querySelector( '.copy-msg' );
			var text = btn.getAttribute( 'data-copy' );
			var done = function() {
				msg.classList.add( 'is-visible' );
				setTimeout( function() {
					msg.classList.remove( 'is-visible' );
				}, 2200 );
			};
			if ( navigator.clipboard ) {
				navigator.clipboard.writeText( text ).then( done, function() {} );
			}
		} );
	} );
} )();
