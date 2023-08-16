<?php
/**
 * The base configuration for WordPress
 *
 * The wp-config.php creation script uses this file during the installation.
 * You don't have to use the web site, you can copy this file to "wp-config.php"
 * and fill in the values.
 *
 * This file contains the following configurations:
 *
 * * Database settings
 * * Secret keys
 * * Database table prefix
 * * ABSPATH
 *
 * @link https://wordpress.org/documentation/article/editing-wp-config-php/
 *
 * @package WordPress
 */

// ** Database settings - You can get this info from your web host ** //
/** The name of the database for WordPress */
define( 'DB_NAME', 'testsite' );

/** Database username */
define( 'DB_USER', 'root' );

/** Database password */
define( 'DB_PASSWORD', '' );

/** Database hostname */
define( 'DB_HOST', 'localhost' );

/** Database charset to use in creating database tables. */
define( 'DB_CHARSET', 'utf8mb4' );

/** The database collate type. Don't change this if in doubt. */
define( 'DB_COLLATE', '' );

/**#@+
 * Authentication unique keys and salts.
 *
 * Change these to different unique phrases! You can generate these using
 * the {@link https://api.wordpress.org/secret-key/1.1/salt/ WordPress.org secret-key service}.
 *
 * You can change these at any point in time to invalidate all existing cookies.
 * This will force all users to have to log in again.
 *
 * @since 2.6.0
 */
define( 'AUTH_KEY',         '8g8|WeDy.jQ{gm$?tOZJ4G=#TA>V(}?PJMK|[fTS<>~@yn$l;6LXeTIX.gTSDmmw' );
define( 'SECURE_AUTH_KEY',  'R1SD]?+qJ~!h$Cp6IR7tn-GT|-K{p[wXAq@{)5IcA*,4co.u?,ha6w~ ?ygx2BXb' );
define( 'LOGGED_IN_KEY',    '6$Wgnb%z>U@|WRupJG[eo}8C+Bxp,x5@G2m<[l}v1.7|.-3JUn-@1*IqF+90mLD!' );
define( 'NONCE_KEY',        'S0A.?-z[>ela:P9}0O:`g7(+tdV/O,,gau57dbif]P}.9}p+`)Pk%CdOk]s;7;jv' );
define( 'AUTH_SALT',        'I@_90q]kpGP~Mn*~R0fj@]OZPw7p5ZOqjy^)e)*bU8Q=71lD|3$M)ZN|srsRcbH[' );
define( 'SECURE_AUTH_SALT', 'wrN7fmi8n8_KOP[fT`LxL!t(=>3&SX_E[s~LK<Rh*B,bYv4/X$QBm, oX W}jnde' );
define( 'LOGGED_IN_SALT',   '%FxYJwlL3[>Z+$OBP(r)I,})zTDj*<Sf7&CDgxW5Z[BT~(D@:G1f.ih+$HC[D^0l' );
define( 'NONCE_SALT',       'a;dbt#YZzzedWl[n|i;[mL&#NstF|qLEQG=Ap}U1p$-SCI7H+8a&!P*Nz^kjxIB~' );

/**#@-*/

/**
 * WordPress database table prefix.
 *
 * You can have multiple installations in one database if you give each
 * a unique prefix. Only numbers, letters, and underscores please!
 */
$table_prefix = 'wp_';

/**
 * For developers: WordPress debugging mode.
 *
 * Change this to true to enable the display of notices during development.
 * It is strongly recommended that plugin and theme developers use WP_DEBUG
 * in their development environments.
 *
 * For information on other constants that can be used for debugging,
 * visit the documentation.
 *
 * @link https://wordpress.org/documentation/article/debugging-in-wordpress/
 */
define( 'WP_DEBUG', false );

/* Add any custom values between this line and the "stop editing" line. */



/* That's all, stop editing! Happy publishing. */

/** Absolute path to the WordPress directory. */
if ( ! defined( 'ABSPATH' ) ) {
	define( 'ABSPATH', __DIR__ . '/' );
}

/** Sets up WordPress vars and included files. */
require_once ABSPATH . 'wp-settings.php';
