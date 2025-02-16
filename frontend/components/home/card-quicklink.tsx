import { Card, CardBody } from "@nextui-org/react";
import React from "react";

interface QuickLinkCardProps {
  href: string;
  logo: React.ReactElement;
  text: string;
}

export const QuickLinkCard: React.FC<QuickLinkCardProps> = ({ href, logo, text }) => {
  // Clone the logo and override its dimensions to fill the container
  const styledLogo = React.cloneElement(logo, {
    // Remove any fixed dimensions so our container rules apply
    width: undefined,
    height: undefined,
    style: {
      ...logo.props.style,
      width: "100%",
      height: "100%",
      objectFit: "contain",
      margin: "auto",
    },
    className: `w-full h-full object-contain block ${logo.props.className || ""}`,
  });

  return (
    <a href={href} target="_blank" rel="noopener noreferrer" className="block">
      <Card className="xl:max-w-sm bg-default-50 rounded-xl shadow-md w-full transition-transform duration-300 hover:scale-105 hover:shadow-lg">
        <CardBody className="py-5 overflow-hidden flex flex-col items-center justify-center">
          {/* Use an aspect ratio container instead of a fixed height */}
          <div
            className="w-full overflow-hidden"
            style={{ aspectRatio: "188 / 56" }}
          >
            {styledLogo}
          </div>
          {/* Spacing between logo and text */}
          <div className="mt-4 w-full">
            <span className="text-default-900 text-xl font-semibold text-center block">
              {text}
            </span>
          </div>
        </CardBody>
      </Card>
    </a>
  );
};
