<!-- mimeremove and mimereject -->
<?cs call:checkbox("x") ?>
	<?cs if:(Data.List.Options.x == 1) ?><ul>
	<!-- turn off mimermove, if "-x" is not activated, as it will be
			removed during the next config_update -->
		<?cs call:display_option('mimereject') ?>
		<?cs call:display_option('mimeremove') ?>
	</ul><?cs /if ?>

