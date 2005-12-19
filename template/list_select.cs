<div id="list_select" class="container">

    <div class="title">
		<h1><?cs var:Lang.Title.ListSelect ?></h1>
    </div>

	<?cs if:(subcount(Data.Lists) > 0) ?>
	<ul>
		<?cs each:item = Data.Lists ?>
			<li><a href="<?cs var:ScriptName ?>?list=<?cs var:url_escape(item)
				?>&action=subscribers"><?cs var:item ?></a></li>
		<?cs /each ?>
	</ul>
	<?cs /if ?>

</div>
