#!/usr/bin/env Rscript
# meal_tip_pie.R
# Create a pie chart splitting a restaurant bill into meal and a 15% tip.
#
# Usage:
#  - Rscript meal_tip_pie.R 45.50    # pass meal cost as command-line argument
#  - or run interactively and enter a value when prompted

args <- commandArgs(trailingOnly = TRUE)
if (length(args) >= 1) {
    meal <- as.numeric(args[1])
} else if (interactive()) {
    meal <- as.numeric(readline("Enter meal cost (e.g. 45.50): "))
} else {
    # Default sample value when no input given
    meal <- 50.00
}

if (is.na(meal) || meal < 0) stop("Invalid meal cost.")

tip_rate <- 0.15
tip <- meal * tip_rate
values <- c(Meal = meal, Tip = tip)
total <- sum(values)
percent <- round(values / total * 100)

labels <- paste0(names(values), "\n$", formatC(values, format = "f", digits = 2),
                                 " (", percent, "%)")

# Save to PNG in current working directory
outfile <- "meal_tip_pie.png"
png(filename = outfile, width = 800, height = 600)
pie(values,
        labels = labels,
        col = c("#4E79A7", "#F28E2B"),
        main = sprintf("Meal vs 15%% Tip — Total: $%0.2f", total),
        clockwise = TRUE,
        border = "white",
        cex = 1.2)
dev.off()

cat(sprintf("Pie chart saved to %s (Meal $%0.2f, Tip $%0.2f)\n", outfile, meal, tip))