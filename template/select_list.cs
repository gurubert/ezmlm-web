<!-- print available lists and administrative buttons -->

<h2>Choose a list to configure</h2>

<?cs if:(Data.ListsCount > 0) ?>
<!-- scrollbox for available lists -->
<div class="list_lists">
    <!-- Keep selection box a resonable size - suggested by Sebastian Andersson -->
    <?cs if:(Data.ListsCount > 25) ?>
	<?cs set:Data.ScrollSize = 25 ?>
      <?cs else ?>
	<?cs set:Data.ScrollSize = Data.ListsCount ?>
    <?cs /if ?>
    <ul>
	<?cs each:item = Data.Lists ?>
	    <li><a href="<?cs var:Data.ScriptName ?>?list=<?cs var:item ?>&action=list_subscribers"><?cs var:item ?></a></li>
	<?cs /each ?>
    </ul>
</div>

<?cs /if ?>
