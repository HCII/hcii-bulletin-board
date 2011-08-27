/*
 * jQuery TinyModal plugin
 * Version 0.1
 *
 * Copyright (c) 2011 Ian Li (http://ianli.com)
 * Licensed under the MIT License (http://www.opensource.org/licenses/mit-license.php).
 */

(function ($) {
	// Coding style of this plugin is based on
	// http://docs.jquery.com/Plugins/Authoring
	
	var methods = {
		// Initializes the modal. The options are:
		// * top
		// * zIndex
		// * opacity
		init: function (options) {
			// To avoid scope issues, use 'self' instead of 'this'
	        // to reference this object from internal events and functions.
			var self = this,
			
			// The jQuery element wrapper to this element.
			$self = $(self),
			
			// Default values for options.
			defaults = {
				top: 100,
				zIndex: 1000000,
				opacity: 0.5
			};
			
			// Merge the options to the defaults,
			// overwriting the attributes defined in defaults.
			options = $.extend(defaults, options);
			
			// This is the overlay:
			// * It appears below the modal and is translucent.
			// * It is spans the whole window.			
			// * Its z-index is 1 less than the z-index of the modal.
			// * Clicking on it closes the modal.
			var overlay = $('<div></div>')
				.css({
					display: 'none',
					position: 'fixed',
					top: '0px',
					left: '0px',
					height: '100%',
					width: '100%',
					background: '#000',
					'z-index': options.zIndex - 1
				})
				.appendTo('body')
				.fadeTo(200, options.opacity)
				.click(function () {
					$self.hide();
					overlay.remove();
				});
		
			var modalWidth = $self.outerWidth();
				
			return $self
					.css({
						'display': 'block',
						'position': 'fixed',
						'top': options.top + 'px',
						'left': 50 + '%',
						'margin-left': -(modalWidth / 2) + 'px',
						'opacity': 0,
						'z-index': options.zIndex
					})					
					.data('tinymodal-overlay', overlay)
					.click(function (event) {
						event.stopPropagation();
					})
					.fadeTo(200, 1);
		},
		
		close: function () {
			var self = this,
				$self = $(self);
			
			$self.hide();
			var overlay = $self.data('tinymodal-overlay');
			if (overlay) {
				overlay.remove();
			}
		},
		
		version: function () {
			return '0.1';
		}
	};
	
	$.fn.tinymodal = function (method) {
		if (methods[method]) {
			return methods[method].apply(this, Array.prototype.slice.call(arguments, 1));
		} else if (typeof method === 'object' || !method) {
			return methods.init.apply(this, arguments);
		} else {
			$.error('Method ' +  method + ' does not exist on jQuery.tinymodal' );
		}
	};
})(jQuery);