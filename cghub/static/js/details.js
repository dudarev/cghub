$(function () {
    collapseAll();

    var collapseButton = $("#id-collapse-all-button");
    var expandButton = $("#id-expand-all-button");
    collapseButton.click(collapseAll);
    expandButton.click(expandAll);

    function collapseAll() {
        var visibleMinuses = $("div.Element:visible > span.Clickable:contains('-')");
        visibleMinuses.each(function(){
            ToggleElementVisibility(this);
        });
    }

    function expandAll() {
        var pluses = $("div.Element > span.Clickable:contains('+')");
        pluses.each(function(){
            ToggleElementVisibility(this);
        });
    }
});
